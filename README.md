# WebUSB_Adaptation (PyUSB)

Use usb_reader.py to launch the PyUSB connection for the COM port.

Instructions on how to install and work with the PyUSB:

1. Create directory
2. Navigate to the directory
3. In the command line:
* pip install pyusb (install pyUSB extension)
* brew install libusb OR pip install libusb1 (install backend)
* python usb_reader.py (run the application)

Technical Documentation:

I. Function Analysis
******************************
simulate_usb_data(data_size=64)
Description:
Generates simulated byte data to mimic data received from a USB device.

Parameters:
* data_size (int, default=64): Desired size of the simulated data byte string.
Returns:
* bytes: A byte string containing the message "Hello, this is simulated data from your device." followed by null bytes to fill up the desired length.
Example:
* print(simulate_usb_data(32))
* Output: b'Hello, this is simulated data\x00\x00\x00\x00\x00\x00'
*****************************
get_usb_data(vendor_id, product_id, endpoint, data_size=64, simulate=False/True)
Description:
Fetches data from a specified USB device. If simulate is set to True, it will return simulated data.

Parameters:
* vendor_id (int): Vendor ID of the target USB device.
* product_id (int): Product ID of the target USB device.
* endpoint (int): The communication endpoint of the USB device.
* data_size (int, default=64): The size of the data expected to be received.
* simulate (bool, default=False): If set to True, the function will return simulated data.
Returns:
* bytes: Data read from the USB device as a byte string.
Throws:
* ValueError: If the USB device with the specified vendor_id and product_id is not found.
Example:
Using simulated data
* data_simulated = get_usb_data(0x1234, 0x5678, 0x81, 64, True)
* print(data_simulated)
* Output: b'Hello, this is simulated data from your device...' (if simulate is True)
*********************************************
Fetching real data from the USB device
Note: The output will vary based on the actual data received from the connected USB device.
* data_real = get_usb_data(0x1234, 0x5678, 0x81, 64, False)
* print(data_real)
* Output: ... (whatever data is currently being sent by the connected USB device)
**********************************************
main()
Description:
* Serves as the primary entry point to the script. Sets up USB device parameters, fetches the data using get_usb_data, and writes the received data to a .txt file.
********************************************
Functionality:
* Defines the USB device parameters (VENDOR_ID, PRODUCT_ID, and ENDPOINT_ADDRESS).
* Calls the get_usb_data function to fetch data. Currently, it's set to fetch simulated data.
* Writes the fetched data into a file named data.txt.
Example:
If script is run as a standalone:
* python script_name.py
* data.txt will be generated/overwritten with the fetched data.
************************************************






