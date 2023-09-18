import usb.core
import usb.util
import serial

def simulate_usb_data(data_size=64):
    # Simulate data from a device
    simulated_data = b"Hello, this is simulated data from your device." + b"\x00" * (data_size - 46)
    return simulated_data

def get_usb_data(vendor_id, product_id, endpoint, data_size=64, simulate=False):
    if simulate:
        return simulate_usb_data(data_size)

    # Find the USB device based on vendor_id and product_id
    dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)

    if dev is None:
        raise ValueError("Device not found")

    # Detach kernel driver if necessary
    if dev.is_kernel_driver_active(0):
        dev.detach_kernel_driver(0)

    # Set the default configuration
    dev.set_configuration()

    # Read data from the device
    data = dev.read(endpoint, data_size)
    
    return data.tobytes()  # convert from array to bytes

def get_uart_data(com_port, baud_rate=115200, data_size=64, simulate=False):
    # Adjusted baud rate for BMP; it often operates at 115200, but you might need to confirm
    if simulate:
        return simulate_usb_data(data_size)

    # Open the COM port
    with serial.Serial(com_port, baud_rate, timeout=1) as ser:
        data = ser.read(data_size)
        
    return data

def main():
    choice = input("Select communication type (USB/UART/BMP): ").upper()
    
    if choice == "USB":
        # Adjust these values to your device
        VENDOR_ID = 0x1234
        PRODUCT_ID = 0x5678
        ENDPOINT_ADDRESS = 0x81  # usually 0x81 or similar for IN endpoint
        data = get_usb_data(VENDOR_ID, PRODUCT_ID, ENDPOINT_ADDRESS, simulate=True)

    elif choice == "UART":
        COM_PORT = 'COM3'  # Adjust this value to your COM port
        BAUD_RATE = 9600   # Baud rate, adjust as per your setup
        data = get_uart_data(COM_PORT, BAUD_RATE, simulate=True)

    elif choice == "BMP":
        BMP_COM_PORT = 'COM4'  # This is an example. You'll need to adjust based on which port BMP UART passthrough is on.
        data = get_uart_data(BMP_COM_PORT, simulate=True)
        
    else:
        print("Invalid choice!")
        return

    # Write the data to a txt file
    with open("data.txt", "wb") as file:
        file.write(data)

if __name__ == "__main__":
    main()
