import serial

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
