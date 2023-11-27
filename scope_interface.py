
#pyusb setup
import usb.core
import usb.util
import usb.backend.libusb1
import sys


# -----------------------  Data Conversion Methods ----------------------- #


def to_bin(sample):
    res = "{0:08b}".format(sample)
    return res

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


# -----------------------  Public Methods ----------------------- #


#backend = usb.backend.libusb1.get_backend(find_library=lambda x: "./libusb-1.0.dll")

#connects to Simple Scope
def connect_to_scope():

    global dev
    #dev = usb.core.find(backend=backend)
    dev = usb.core.find(idVendor=0x1FC9, idProduct=0x008A) #idProduct=0x008A for programmed device

    if dev is None:
        raise ValueError('Simple Scope is not connected!')
    else:
        print("Simple Scope Connected!")

    #print(dev)

    cfg = usb.util.find_descriptor(dev, bConfigurationValue=1)
    cfg.set()

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

#inputs in_tokens into scope BULK_IN endpoint
#returns data buffer of signed integers
def get_samples():
    samples = []
    sample_temp = []
    samples_bin = []
    for i in range(1024):
        data = dev.read(0x81, 0x40, 1000)
        #print(str(i) + " " + str(data))
        sample_temp.extend(data)

    datasize = len(sample_temp)

    for j in range(0, datasize-1, 2):
        b0 = to_bin(sample_temp[j])     #convert lower int to 8-bit binary
        b1 = to_bin(sample_temp[j+1])   #convert upper int to 8-bit binary

        sample_12b = "".join([b1[4:8], b0])     #concatenate into 12-bit sample value (truncate upper 4-bits)
        samples_bin.append(sample_12b)

        point = twos_comp(int(sample_12b,2), len(sample_12b))
        samples.append(point)

        #print(samples_bin)

    return samples

#polls scope INTERRUPT endpoint for new data
#returns status bit
def check_for_data():
    res = dev.read(0x82, 0x4, 0x8)
    return res

#sends array of user configuration values to scope BULK_OUT endpoint
def configure_scope(user_configs):
    dev.write(0x01, user_configs)

