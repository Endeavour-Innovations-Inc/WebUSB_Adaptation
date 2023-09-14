import usb.core
import usb.util

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

def main():
    # Adjust these values to your device
    VENDOR_ID = 0x1234
    PRODUCT_ID = 0x5678
    ENDPOINT_ADDRESS = 0x81  # usually 0x81 or similar for IN endpoint
    
    data = get_usb_data(VENDOR_ID, PRODUCT_ID, ENDPOINT_ADDRESS, simulate=True)

    # Write the data to a txt file
    with open("data.txt", "wb") as file:
        file.write(data)

if __name__ == "__main__":
    main()
