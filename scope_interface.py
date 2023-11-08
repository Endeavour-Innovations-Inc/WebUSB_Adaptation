import serial
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
dev = usb.core.find(idVendor=0x1FC9, idProduct=0x000C)

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
    for i in range(8):
        while True:
            try:
                #dev.write(0x82, 'prime', 1000)     #uncomment this line to manually write a value into the interrupt endpoint
                data = dev.read(0x81, 0x40, 1000)
            except usb.core.USBTimeoutError as e:
                data = None
                print('Timeout encountered - continuing')
                continue
        print(data)
        samples.extend(data)
    return samples

    

def configure_scope(user_config):
    dev.write(0x81, user_config)


# ----------------------- serial port example ----------------------- #

"""
def simulate_uart_data(data_size=64):
    # Simulate data from a UART device
    simulated_data = b"Hello, this is simulated data from UART." + b"\x00" * (data_size - 48)
    return simulated_data

def get_uart_data(com_port, baud_rate=115200, data_size=64, simulate=False):
    if simulate:
        return simulate_uart_data(data_size)

    # Open the COM port
    with serial.Serial(com_port, baud_rate, timeout=1) as ser:
        data = ser.read(data_size)

    return data

def main():
    choice = input("Select communication type (UART/BMP): ").upper()

    if choice == "UART":
        COM_PORT = 'COM3'  # Adjust this value to your COM port
        BAUD_RATE = 9600   # Baud rate, adjust as per your setup
        data = get_uart_data(COM_PORT, BAUD_RATE, simulate=True)

    elif choice == "BMP":
        BMP_COM_PORT = 'COM4'  # This is an example. You'll need to adjust based on which port BMP UART passthrough is on.
        data = get_uart_data(BMP_COM_PORT, simulate=True)

    else:
        print("Invalid choice!")
        return

    # Append the data to a txt file on a new line
    with open("data.txt", "ab") as file:
        file.write(data + b'\n')  # Appending a newline byte to the end of the data

if __name__ == "__main__":
    main()
"""
