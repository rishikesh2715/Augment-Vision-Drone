import serial

# Open the serial port (use your COM port)
ser = serial.Serial('COM7', 115200, timeout=1)  # replace 'COM1' with your COM port

while True:
    # Read a byte from the serial port
    byte = ser.read()
    # print(byte)

    # Print the byte as a hex number
    print(byte.hex())






# import serial
# import struct

# def process_frame(frame):
#     # Frame structure: <Type> <Payload> <CRC>
#     frame_type = frame[0]
#     payload = frame[1:-1]
#     crc = frame[-1]

#     # Process frame based on its type
#     # This is where you would add your code to handle the different frame types
#     print(f"Frame type: {frame_type}, Payload: {payload}, CRC: {crc}")

# ser = serial.Serial('COM7', 115200, timeout=1)  # replace 'COM1' with your COM port

# buffer = b""

# while True:
#     # Read a byte from the serial port
#     byte = ser.read()
#     buffer += byte

#     # If the buffer contains the device address and at least one more byte (the frame length), we can start processing a frame
#     if buffer.startswith(b"\xea") and len(buffer) > 1:
#         # Get the frame length
#         frame_length = buffer[1]

#         # If the buffer contains the whole frame, process it
#         if len(buffer) >= frame_length + 2:  # Add 2 for the device address and the frame length byte
#             frame = buffer[2:frame_length+2]  # Get the frame data
#             process_frame(frame)

#             # Remove the processed frame from the buffer
#             buffer = buffer[frame_length+2:]
