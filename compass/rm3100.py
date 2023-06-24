import serial
import time
from math import sqrt

# Configure the serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # Update the port and baud rate based on your setup

def process_data(x, y, z):
    # Perform your desired calculations here
    uT = sqrt(((x / gain) ** 2) + ((y / gain) ** 2) + ((z / gain) ** 2))
    print("Data in counts: X:", x, "Y:", y, "Z:", z)
    print("Data in microTesla(uT): X:", x / gain, "Y:", y / gain, "Z:", z / gain)
    print("Magnitude(uT):", uT)
    print()

def main():
    while True:
        data = read_data()
        if data is not None:
            x, y, z = data
            # Process the x, y, and z values here
            print(f"X: {x}, Y: {y}, Z: {z}")

def read_data():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()  # Read a line from the serial connection
            values = line.split(',')  # Split the line into individual values
            print(values[0])
            if len(values) == 3:
                x, y, z = map(float, values)  # Convert the values to floats
                return x, y, z
        except (UnicodeDecodeError, ValueError):
            pass  # Ignore decoding and value errors and continue reading


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()  # Close the serial connection when done
