import numpy as np
import sample_convert

# -----------------------  USB example ----------------------- #

#pyusb setup
import usb.core
import usb.util
import usb.backend.libusb1
import sys

backend = usb.backend.libusb1.get_backend(find_library=lambda x: "./libusb-1.0.dll")

dev = usb.core.find(backend=backend)
dev = usb.core.find(idVendor=0x1FC9, idProduct=0x008A)

if dev is None:
    raise ValueError('Simple Scope is not connected!')
else:
    print("Simple Scope Connected!")

print(dev)

cfg = usb.util.find_descriptor(dev, bConfigurationValue=1)
cfg.set()


#get first ENDPOINT_OUT address
"""
# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)
eaddr = ep.bEndpointAddress
"""


#print(cfg)

try:
    dev.set_interface_altsetting(interface = 0, alternate_setting = 0x0)
except usb.core.USBError:
    pass


#Device control transfer request
"""
def get_device_info():
    for bRequest in range(255):
        try:
            read = dev.ctrl_transfer(0x80, bRequest, 0, 0, 16) #read 8 bytes
            print ("bRequest ", bRequest)
            print (read)
        except:
            # failed to get data for this request
            pass
"""

def get_samples():
    samples = []
    for i in range(1024):
        """
        while True:
            try:
                #dev.write(0x82, 'prime', 1000)     #uncomment this line to manually write a value into the interrupt endpoint
                data = dev.read(0x81, 0x40, 1000)
                print(i + " " + data)
            except usb.core.USBTimeoutError as e:
                data = None
                print(str(e) + ' - continuing')
                pass
        """
        data = dev.read(0x81, 0x40, 1000)
        print(str(i) + " " + str(data))
        samples.extend(data)
        #print(samples)
    return samples


def configure_scope(user_config):
    dev.write(0x01, user_config)


def to_dec(sample):
    print(sample)
    res = "{0:012b}".format(int(sample, 16))
    print(res)
    dec = twos_comp(int(res, 2), len(res))

    return dec

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


