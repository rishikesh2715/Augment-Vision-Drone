import serial
import struct

def processSerialData(drone):
    
    # Constants
    RADIO_ADDRESS = 0xea

    # Open serial port
    # ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser = serial.Serial('COM7', 57600)
    if not ser.is_open():
        ser.open()


    crc8_dvb_s2_table = [
        0x00, 0xD5, 0x7F, 0xAA, 0xFE, 0x2B, 0x81, 0x54, 0x29, 0xFC, 0x56, 0x83, 0xD7, 0x02, 0xA8, 0x7D,
        0x52, 0x87, 0x2D, 0xF8, 0xAC, 0x79, 0xD3, 0x06, 0x7B, 0xAE, 0x04, 0xD1, 0x85, 0x50, 0xFA, 0x2F,
        0xA4, 0x71, 0xDB, 0x0E, 0x5A, 0x8F, 0x25, 0xF0, 0x8D, 0x58, 0xF2, 0x27, 0x73, 0xA6, 0x0C, 0xD9,
        0xF6, 0x23, 0x89, 0x5C, 0x08, 0xDD, 0x77, 0xA2, 0xDF, 0x0A, 0xA0, 0x75, 0x21, 0xF4, 0x5E, 0x8B,
        0x9D, 0x48, 0xE2, 0x37, 0x63, 0xB6, 0x1C, 0xC9, 0xB4, 0x61, 0xCB, 0x1E, 0x4A, 0x9F, 0x35, 0xE0,
        0xCF, 0x1A, 0xB0, 0x65, 0x31, 0xE4, 0x4E, 0x9B, 0xE6, 0x33, 0x99, 0x4C, 0x18, 0xCD, 0x67, 0xB2,
        0x39, 0xEC, 0x46, 0x93, 0xC7, 0x12, 0xB8, 0x6D, 0x10, 0xC5, 0x6F, 0xBA, 0xEE, 0x3B, 0x91, 0x44,
        0x6B, 0xBE, 0x14, 0xC1, 0x95, 0x40, 0xEA, 0x3F, 0x42, 0x97, 0x3D, 0xE8, 0xBC, 0x69, 0xC3, 0x16,
        0xEF, 0x3A, 0x90, 0x45, 0x11, 0xC4, 0x6E, 0xBB, 0xC6, 0x13, 0xB9, 0x6C, 0x38, 0xED, 0x47, 0x92,
        0xBD, 0x68, 0xC2, 0x17, 0x43, 0x96, 0x3C, 0xE9, 0x94, 0x41, 0xEB, 0x3E, 0x6A, 0xBF, 0x15, 0xC0,
        0x4B, 0x9E, 0x34, 0xE1, 0xB5, 0x60, 0xCA, 0x1F, 0x62, 0xB7, 0x1D, 0xC8, 0x9C, 0x49, 0xE3, 0x36,
        0x19, 0xCC, 0x66, 0xB3, 0xE7, 0x32, 0x98, 0x4D, 0x30, 0xE5, 0x4F, 0x9A, 0xCE, 0x1B, 0xB1, 0x64,
        0x72, 0xA7, 0x0D, 0xD8, 0x8C, 0x59, 0xF3, 0x26, 0x5B, 0x8E, 0x24, 0xF1, 0xA5, 0x70, 0xDA, 0x0F,
        0x20, 0xF5, 0x5F, 0x8A, 0xDE, 0x0B, 0xA1, 0x74, 0x09, 0xDC, 0x76, 0xA3, 0xF7, 0x22, 0x88, 0x5D,
        0xD6, 0x03, 0xA9, 0x7C, 0x28, 0xFD, 0x57, 0x82, 0xFF, 0x2A, 0x80, 0x55, 0x01, 0xD4, 0x7E, 0xAB,
        0x84, 0x51, 0xFB, 0x2E, 0x7A, 0xAF, 0x05, 0xD0, 0xAD, 0x78, 0xD2, 0x07, 0x53, 0x86, 0x2C, 0xF9]

    def crc8_dvb_s2(data):
        crc = 0
        #print(f'Length of CRC table: {len(crc8_dvb_s2_table)}')  # Debugging line
        for i, byte in enumerate(data):
            #print(f'iteration: {i}, crc: {crc}, byte: {byte}')   # Debugging line
            crc = crc8_dvb_s2_table[crc ^ byte] 
        return crc


    while True:
        # Read a byte
        device_address = ser.read(1)

        # Check if it's the start of a new frame
        if ord(device_address) == RADIO_ADDRESS:
            # Read frame length
            frame_length = struct.unpack('<B', ser.read(1))[0]

            # Read frame type
            frame_type = struct.unpack('<B', ser.read(1))[0]

            # Read payload
            payload = ser.read(frame_length - 2)  # subtract 2 for frame type and CRC

            # Read CRC
            crc = struct.unpack('<B', ser.read(1))[0]
            
            # Validate CRC
            calculated_crc = crc8_dvb_s2(bytes([frame_type]) + payload)
            if calculated_crc != crc:
                print("CRC error: calculated CRC does not match received CRC. Data may be corrupted.")


            if frame_type == 0x02:  # GPS
                drone.lat, drone.lon, drone.speed, drone.heading, drone.altitude, drone.sats = struct.unpack('>iiHHHB', payload)
                drone.lat /= 1e7              # degrees
                drone.lon /= 1e7              # degrees
                drone.speed /= 10             # km/h
                drone.heading /= 100          # degrees
                drone.altitude -= 1000        # meters
                # print(f'GPS: Lat={drone.lat}, drone.Lon={drone.lon}, drone.Speed={drone.speed}, drone.heading={drone.heading}, drone.Altitude={drone.altitude}, drone.Sats={drone.sats}')

            elif frame_type == 0x07:  # VARIO
                vertical_speed = struct.unpack('>h', payload)[0]
                # print(f'VARIO: Vertical speed={vertical_speed}')

            
            elif frame_type == 0x08:  # Battery
                voltage, current = struct.unpack('>HH', payload[:4])
                used = int.from_bytes(payload[4:7], byteorder='big') # manually unpack 3-byte integer
                remaining = struct.unpack('>B', payload[7:])[0]
                voltage /= 10            # volts
                current /= 10          # amps
                # print(f'Battery: Voltage={voltage}, Current={current}, Used={used}, Remaining={remaining}')


            elif frame_type == 0x14:  # Link Statistics
                # Unpack data
                data = struct.unpack('>BBBBBBBbbb', payload)
                # print(f'Link Statistics: Uplink RSSI Ant. 1={data[0]}, Uplink RSSI Ant. 2={data[1]}, Uplink Package success rate / Link quality={data[2]}, Uplink SNR={data[3]}, Diversity active antenna={data[4]}, RF Mode={data[5]}, Uplink TX Power={data[6]}, Downlink RSSI={data[7]}, Downlink package success rate / Link quality={data[8]}, Downlink SNR={data[9]}')
                uplink_rssi_ant1, uplink_rssi_ant2, uplink_quality, uplink_snr, active_antenna, rf_mode, uplink_tx_power, downlink_rssi, downlink_quality, downlink_snr = struct.unpack('>bbbBbbbbbB', payload)
                uplink_rssi_ant1 /= -1
                uplink_rssi_ant2 /= -1
                downlink_rssi /= -1
                # print(f'Link Statistics: Uplink RSSI Ant.1={uplink_rssi_ant1}dBm, Uplink RSSI Ant.2={uplink_rssi_ant2}dBm, Uplink Quality={uplink_quality}%, Uplink SNR={uplink_snr}db, Active Antenna={active_antenna}, RF Mode={rf_mode}, Uplink TX Power={uplink_tx_power}, Downlink RSSI={downlink_rssi}dBm, Downlink Quality={downlink_quality}%, Downlink SNR={downlink_snr}db')
            
            elif frame_type == 0x1e:  # Attitude
                drone.pitch, drone.roll, drone.yaw = struct.unpack('>hhh', payload)
                drone.pitch /= 10000           # degrees
                drone.roll /= 10000            # degrees
                drone.yaw /= 10000             # degrees
                print(f'Attitude: drone.Pitch={drone.pitch}, drone.Roll={drone.roll}, drone.Yaw={drone.yaw}')

            elif frame_type == 0x1e:  # Attitude
                drone.pitch = float((payload[0] << 8) + payload[1]) / 1000
                drone.roll = float((payload[2] << 8) + payload[3]) / 1000
                drone.yaw = float((payload[4] << 8) + payload[5]) / 1000
                print(f'Attitude: drone.Pitch={drone.pitch}, drone.Roll={drone.roll}, drone.Yaw={drone.yaw}')


            elif frame_type == 0x21:  # Flight Mode
                flight_mode = payload.decode('ascii').rstrip('\x00')
                # print(f'Flight Mode: {flight_mode}')

            elif frame_type == 0x29:  # Device Info
                destination, origin = struct.unpack('<BB', payload[:2])
                device_name = payload[2:].decode('ascii').rstrip('\x00')
                # print(f'Device Info: Destination={destination}, Origin={origin}, Device Name={device_name}')

            else:
                # print(f'Unknown frame type: {frame_type}')
                pass

        else:
            print(f'Unknown device address: {device_address}')


