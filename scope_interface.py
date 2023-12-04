
import usb.core
import usb.util
import usb.backend.libusb1
import sys

import subprocess


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

def program_scope():
    subprocess.run(["powershell", "./LPCScrypt_2.1.2_57/scripts/boot_lpcscrypt.cmd ./LPCScrypt_2.1.2_57/BufferTest.bin.hdr"], shell=True)


dev = None
backend = usb.backend.libusb1.get_backend(find_library=lambda x: "./libusb-1.0.dll")

#connects to Simple Scope
def connect_to_scope():

    global dev
    dev = usb.core.find(backend=backend)
    dev = usb.core.find(idVendor=0x1FC9, idProduct=0x008A) #idProduct=0x008A for programmed device

    if dev is None:
        raise ValueError('Simple Scope is not connected!')
    else:
        print("#\n#\n#\n# -----------------------  Simple Scope Connected! ----------------------- \n#\n#\n#")

    #print(dev)

    cfg = usb.util.find_descriptor(dev, bConfigurationValue=1)
    cfg.set()

    try:
        dev.set_interface_altsetting(interface = 0, alternate_setting = 0x0)
    except usb.core.USBError:
        pass

#inputs in_tokens into scope BULK_IN endpoint
#returns data buffer of signed integers
index_buff = []
index = 0
def get_samples():
    
    index_buff = dev.read(0x81, 0x40, 1000)
    index = "".join([to_bin(index_buff[3]), to_bin(index_buff[2]), to_bin(index_buff[1]), to_bin(index_buff[0])])
    #index = "".join([to_bin(index_buff[0]), to_bin(index_buff[1]), to_bin(index_buff[2]), to_bin(index_buff[3])])  #uncomment line if order is backwards
    #print(index_buff)
    #print(index)
    
    samples = []
    sample_temp = []
    samples_bin = []
    for i in range(1792):
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

    #arrange samples based on starting index
    split1 = samples[0:int(index,2)]
    split2 = samples[int(index,2):len(samples)]
    split2.extend(split1)

    return split2

#polls scope INTERRUPT endpoint for new data
#returns status bit
def check_for_data():
    res = dev.read(0x82, 0x4, 0x8)
    return res

#sends array of user configuration values to scope BULK_OUT endpoint
def configure_scope(user_configs):
    if dev is None:
        raise ValueError('Simple Scope is not connected!')
    else:
        dev.write(0x01, user_configs)

