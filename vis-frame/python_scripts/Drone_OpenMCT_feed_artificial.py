# import socket
# import time
# from serial import Serial
# import struct
# import math

# # Constants for UDP sender
# UDP_IP = "127.0.0.1"  # standard ip udp (localhost)
# UDP_PORT = 50020  # chosen port to OpenMCT (same as in telemetry server object)
keys = [
    "gps.lat",
    "gps.lon",
    "gps.speed",
    "gps.heading",
    "gps.altitude",
    "gps.sats",
    "gps.vario",
    "drone.voltage",
    "drone.current",
    "batt.used",
    "batt.remaining",
    "rssi.uplink.ant1",
    "rssi.uplink.ant2",
    "rssi.uplink.quality",
    "rssi.uplink.snr",
    "rssi.no.antenna",
    "rf.mode",
    "rf.txpower",
    "rssi.downlink",
    "rssi.downlink.quality",
    "rssi.downlink.snr",
    "drone.pitch",
    "drone.roll",
    "drone.yaw",
    "drone.flightmode",
]

# # Constants for Serial Reader
# RADIO_ADDRESS = 0xea
# ser = Serial('COM7', 115200)


# crc8_dvb_s2_table = [
#     0x00, 0xD5, 0x7F, 0xAA, 0xFE, 0x2B, 0x81, 0x54, 0x29, 0xFC, 0x56, 0x83, 0xD7, 0x02, 0xA8, 0x7D,
#     0x52, 0x87, 0x2D, 0xF8, 0xAC, 0x79, 0xD3, 0x06, 0x7B, 0xAE, 0x04, 0xD1, 0x85, 0x50, 0xFA, 0x2F,
#     0xA4, 0x71, 0xDB, 0x0E, 0x5A, 0x8F, 0x25, 0xF0, 0x8D, 0x58, 0xF2, 0x27, 0x73, 0xA6, 0x0C, 0xD9,
#     0xF6, 0x23, 0x89, 0x5C, 0x08, 0xDD, 0x77, 0xA2, 0xDF, 0x0A, 0xA0, 0x75, 0x21, 0xF4, 0x5E, 0x8B,
#     0x9D, 0x48, 0xE2, 0x37, 0x63, 0xB6, 0x1C, 0xC9, 0xB4, 0x61, 0xCB, 0x1E, 0x4A, 0x9F, 0x35, 0xE0,
#     0xCF, 0x1A, 0xB0, 0x65, 0x31, 0xE4, 0x4E, 0x9B, 0xE6, 0x33, 0x99, 0x4C, 0x18, 0xCD, 0x67, 0xB2,
#     0x39, 0xEC, 0x46, 0x93, 0xC7, 0x12, 0xB8, 0x6D, 0x10, 0xC5, 0x6F, 0xBA, 0xEE, 0x3B, 0x91, 0x44,
#     0x6B, 0xBE, 0x14, 0xC1, 0x95, 0x40, 0xEA, 0x3F, 0x42, 0x97, 0x3D, 0xE8, 0xBC, 0x69, 0xC3, 0x16,
#     0xEF, 0x3A, 0x90, 0x45, 0x11, 0xC4, 0x6E, 0xBB, 0xC6, 0x13, 0xB9, 0x6C, 0x38, 0xED, 0x47, 0x92,
#     0xBD, 0x68, 0xC2, 0x17, 0x43, 0x96, 0x3C, 0xE9, 0x94, 0x41, 0xEB, 0x3E, 0x6A, 0xBF, 0x15, 0xC0,
#     0x4B, 0x9E, 0x34, 0xE1, 0xB5, 0x60, 0xCA, 0x1F, 0x62, 0xB7, 0x1D, 0xC8, 0x9C, 0x49, 0xE3, 0x36,
#     0x19, 0xCC, 0x66, 0xB3, 0xE7, 0x32, 0x98, 0x4D, 0x30, 0xE5, 0x4F, 0x9A, 0xCE, 0x1B, 0xB1, 0x64,
#     0x72, 0xA7, 0x0D, 0xD8, 0x8C, 0x59, 0xF3, 0x26, 0x5B, 0x8E, 0x24, 0xF1, 0xA5, 0x70, 0xDA, 0x0F,
#     0x20, 0xF5, 0x5F, 0x8A, 0xDE, 0x0B, 0xA1, 0x74, 0x09, 0xDC, 0x76, 0xA3, 0xF7, 0x22, 0x88, 0x5D,
#     0xD6, 0x03, 0xA9, 0x7C, 0x28, 0xFD, 0x57, 0x82, 0xFF, 0x2A, 0x80, 0x55, 0x01, 0xD4, 0x7E, 0xAB,
#     0x84, 0x51, 0xFB, 0x2E, 0x7A, 0xAF, 0x05, 0xD0, 0xAD, 0x78, 0xD2, 0x07, 0x53, 0x86, 0x2C, 0xF9]

# def crc8_dvb_s2(data):
#     crc = 0
#     #print(f'Length of CRC table: {len(crc8_dvb_s2_table)}')  # Debugging line
#     for i, byte in enumerate(data):
#         #print(f'iteration: {i}, crc: {crc}, byte: {byte}')   # Debugging line
#         crc = crc8_dvb_s2_table[crc ^ byte] 
#     return crc


# # initiate socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP

# data = {}
# for key in keys:
#     data[key] = 0  # Initialize all fields with 0

# while True:
#     # Read a byte
#     device_address = ser.read(1)

#     # Check if it's the start of a new frame
#     if ord(device_address) == RADIO_ADDRESS:
#         # Read frame length
#         frame_length = struct.unpack('<B', ser.read(1))[0]

#         # Read frame type
#         frame_type = struct.unpack('<B', ser.read(1))[0]

#         # Read payload
#         payload = ser.read(frame_length - 2)  # subtract 2 for frame type and CRC

#         # Read CRC
#         crc = struct.unpack('<B', ser.read(1))[0]
        
#         # Validate CRC
#         calculated_crc = crc8_dvb_s2(bytes([frame_type]) + payload)
#         if calculated_crc != crc:
#             print("CRC error: calculated CRC does not match received CRC. Data may be corrupted.")


#         if frame_type == 0x02:  # GPS
#             lat, lon, speed, heading, altitude, sats = struct.unpack('>iiHHHB', payload)
#             lat /= 1e7              # degrees
#             lon /= 1e7              # degrees
#             speed /= 10             # km/h
#             heading /= 100          # degrees
#             altitude -= 1000        # meters

#             # Update data dictionary
#             data["gps.lat"] = lat
#             data["gps.lon"] = lon
#             data["gps.speed"] = speed
#             data["gps.heading"] = heading
#             data["gps.altitude"] = altitude
#             data["gps.sats"] = sats

#             # print(f'GPS: Lat={lat}, Lon={lon}, Speed={speed}, Heading={heading}, Altitude={altitude}, Sats={sats}')
                        
#         elif frame_type == 0x07:  # VARIO
#             vertical_speed = struct.unpack('>h', payload)[0]

#             # Update data dictionary
#             data["gps.vario"] = vertical_speed

#             # print(f'VARIO: Vertical speed={vertical_speed}')

        
#         elif frame_type == 0x08:  # Battery
#             voltage, current = struct.unpack('>HH', payload[:4])
#             used = int.from_bytes(payload[4:7], byteorder='big') # manually unpack 3-byte integer
#             remaining = struct.unpack('>B', payload[7:])[0]
#             voltage /= 10            # volts
#             current /= 10          # amps
#             used = abs(used / 100)        # milliamp hours

#             # Update data dictionary
#             data["drone.voltage"] = voltage
#             data["drone.current"] = current
#             data["batt.used"] = used
#             data["batt.remaining"] = remaining
            
#             # print(f'Battery: Voltage={voltage}, Current={current}, Used={used}, Remaining={remaining}')


        # elif frame_type == 0x14:  # Link Statistics
        #     # Unpack data
        #     # data = struct.unpack('>BBBBBBBbbb', payload)
        #     # print(f'Link Statistics: Uplink RSSI Ant. 1={data[0]}, Uplink RSSI Ant. 2={data[1]}, Uplink Package success rate / Link quality={data[2]}, Uplink SNR={data[3]}, Diversity active antenna={data[4]}, RF Mode={data[5]}, Uplink TX Power={data[6]}, Downlink RSSI={data[7]}, Downlink package success rate / Link quality={data[8]}, Downlink SNR={data[9]}')
        #     uplink_rssi_ant1, uplink_rssi_ant2, uplink_quality, uplink_snr, active_antenna, rf_mode, uplink_tx_power, downlink_rssi, downlink_quality, downlink_snr = struct.unpack('>bbbBbbbbbB', payload)
        #     uplink_rssi_ant1 /= -1
        #     uplink_rssi_ant2 /= -1
        #     downlink_rssi /= -1

        #     # Update data dictionary
        #     data["rssi.uplink.ant1"] = uplink_rssi_ant1
        #     data["rssi.uplink.ant2"] = uplink_rssi_ant2
        #     data["rssi.uplink.quality"] = uplink_quality
        #     data["rssi.uplink.snr"] = uplink_snr
        #     data["rssi.no.antenna"] = active_antenna
        #     data["rf.mode"] = rf_mode
        #     data["rf.txpower"] = uplink_tx_power
        #     data["rssi.downlink"] = downlink_rssi
        #     data["rssi.downlink.quality"] = downlink_quality
        #     data["rssi.downlink.snr"] = downlink_snr

#             # print(f'Link Statistics: Uplink RSSI Ant.1={uplink_rssi_ant1}dBm, Uplink RSSI Ant.2={uplink_rssi_ant2}dBm, Uplink Quality={uplink_quality}%, Uplink SNR={uplink_snr}db, Active Antenna={active_antenna}, RF Mode={rf_mode}, Uplink TX Power={uplink_tx_power}, Downlink RSSI={downlink_rssi}dBm, Downlink Quality={downlink_quality}%, Downlink SNR={downlink_snr}db')
        
#         # elif frame_type == 0x1e:  # Attitude
#         #     pitch, roll, yaw = struct.unpack('>hhh', payload)
#         #     pitch /= 10000           # degrees
#         #     roll /= 10000            # degrees
#         #     yaw /= 10000             # degrees

#         #     # Update data dictionary
#         #     data["drone.pitch"] = pitch
#         #     data["drone.roll"] = roll
#         #     data["drone.yaw"] = yaw

#         #     print(f'Attitude: Pitch={pitch}, Roll={roll}, Yaw={yaw}')

#         elif frame_type == 0x1e:  # Attitude
#                 pitch = float((payload[0] << 8) + payload[1]) / 10000
#                 roll = float((payload[2] << 8) + payload[3]) / 10000
#                 yaw = float((payload[4] << 8) + payload[5]) / 10000
#                 print("[Attitude] pitch=%.3f roll=%.3f yaw=%.3f" % (pitch, roll, yaw))


#         elif frame_type == 0x21:  # Flight Mode
#             flight_mode = payload.decode('ascii').rstrip('\x00')

#             # Update data dictionary
#             data["drone.flightmode"] = flight_mode

#             # print(f'Flight Mode: {flight_mode}')

#         elif frame_type == 0x29:  # Device Info
#             destination, origin = struct.unpack('<BB', payload[:2])
#             device_name = payload[2:].decode('ascii').rstrip('\x00')
#             # print(f'Device Info: Destination={destination}, Origin={origin}, Device Name={device_name}')

#         else:
#             # print(f'Unknown frame type: {frame_type}')
#             pass

#     else:
#         print(f'Unknown device address: {device_address}')
    
#     for key in data:
#         timeStamp = time.time()
#         # built message
#         MESSAGE = "{},{},{}".format(key, data[key], timeStamp)
#         # Pumping out the values
#         sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

#         # print your message for validation and wait for the next loop
#         # print(MESSAGE)

#     time.sleep(0.1)




import socket
import time
from serial import Serial
import struct



# Constants for UDP sender
keys = [
    "gps.lat",
    "gps.lon",
    "gps.speed",
    "gps.heading",
    "gps.altitude",
    "gps.sats",
    "gps.vario",
    "drone.voltage",
    "drone.current",
    "batt.used",
    "batt.remaining",
    "rssi.uplink.ant1",
    "rssi.uplink.ant2",
    "rssi.uplink.quality",
    "rssi.uplink.snr",
    "rssi.no.antenna",
    "rf.mode",
    "rf.txpower",
    "rssi.downlink",
    "rssi.downlink.quality",
    "rssi.downlink.snr",
    "drone.pitch",
    "drone.roll",
    "drone.yaw",
    "drone.flightmode",
]

# CRC8 implementation with polynom = x^8+x^7+x^6+x^4+x^2+1 (0xD5)
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

class DroneTelemetry:
    RADIO_ADDRESS = 0xEA
    FRAME_TYPES = {
    0x02: "parse_gps",
    0x08: "parse_battery",
    0x10: "parse_vtx_telem",
    0x14: "parse_link_statistics",
    0x16: "parse_channels",
    0x1E: "parse_attitude",
    0x21: "parse_flight_mode",
    0x28: "parse_ping_devices",
    0x29: "parse_device",
    0x2a: "parse_fields_request",
    0x2b: "parse_field",
    0x2c: "parse_field_request",
    0x2d: "parse_field_update",
    0x2e: "parse_elrs_info",
    0x32: "parse_command",
    0x3a: "parse_radio_id",
}


    def __init__(self, port='COM7', baudrate=115200, udp_ip="127.0.0.1", udp_port=50020):
        self.ser = Serial(port, baudrate)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Internet, UDP
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.data = {key: 0 for key in keys}
    
    @staticmethod
    def crc8_dvb_s2(data):
        crc = 0
        for byte in data:
            crc = crc8_dvb_s2_table[crc ^ byte] 
        return crc

    def process_serial_data(self):
        while True:
            # Only read the next byte if it's from the RADIO_ADDRESS
            device_address = self.ser.read(1)
            if ord(device_address) == self.RADIO_ADDRESS:
                self.parse_packet()
            else:
                print(f'Unknown device address: {device_address}')

            # Optional: send data after every packet read; tweak depending on use case
            # self.send_to_udp()

            # Small delay to prevent tight loop that hogs CPU resources
            time.sleep(0.1)  # Adjust sleep time as needed

    def parse_packet(self):
        frame_length = struct.unpack('<B', self.ser.read(1))[0]
        frame_type = struct.unpack('<B', self.ser.read(1))[0]
        payload = self.ser.read(frame_length - 2)
        crc = struct.unpack('<B', self.ser.read(1))[0]
        calculated_crc = self.crc8_dvb_s2(bytes([frame_type]) + payload)
        if calculated_crc != crc:
            print("CRC error: calculated CRC does not match received CRC. Data may be corrupted.")
        else:
            self.parse_payload(frame_type, payload)

    def parse_payload(self, frame_type, payload):
        if frame_type in DroneTelemetry.FRAME_TYPES:
            method_name = DroneTelemetry.FRAME_TYPES[frame_type]
            method = getattr(self, method_name, lambda x: "Invalid frame type")
            method(payload)
        else:
            print(f'Unknown frame type: {frame_type}')

    """
    Parsing All the telemetry data 
    """
    # parsing gps data (0x02)
    def parse_gps(self, payload):
        lat, lon, speed, heading, altitude, sats = struct.unpack('>iiHHHB', payload)
        # Convert and store the data in the dictionary
        self.data["gps.lat"] = lat / 1e7
        self.data["gps.lon"] = lon / 1e7
        self.data["gps.speed"] = speed / 100
        self.data["gps.heading"] = heading / 100
        self.data["gps.altitude"] = altitude - 1000
        self.data["gps.sats"] = sats

    def parse_battery(self, payload):
        voltage, current = struct.unpack('>HH', payload[:4])
        used = int.from_bytes(payload[4:7], byteorder='big')
        remaining = struct.unpack('>B', payload[7:])[0]
        # Convert and store the data in the dictionary
        self.data["drone.voltage"] = voltage / 10
        self.data["drone.current"] = current / 10
        self.data["batt.used"] = used / 1000
        self.data["batt.remaining"] = remaining


    def parse_vtx_telem(self, payload):
        return "[VTX Telemetry] freq=%d, power=%d, pitmode=%d" % (int.from_bytes(payload[1:3], 'big'), int(payload[3]), int(payload[4]))
    

    def parse_link_statistics(self, payload):
        if len(payload) != 10:
            print(f"Invalid payload length for Link Statistics: expected 10, got {len(payload)}")
            return
        # Unpack data from payload
        unpacked_data = struct.unpack('>bbbBbbbbbB', payload)
        # Map the unpacked data to their corresponding keys
        self.data["rssi.uplink.ant1"] = unpacked_data[0] * -1  # Assuming RSSI values are negative
        self.data["rssi.uplink.ant2"] = unpacked_data[1] * -1
        self.data["rssi.uplink.quality"] = unpacked_data[2]
        self.data["rssi.uplink.snr"] = unpacked_data[3]
        self.data["rssi.no.antenna"] = unpacked_data[4]  # Assuming this is the active antenna index
        self.data["rf.mode"] = unpacked_data[5]
        self.data["rf.txpower"] = unpacked_data[6]
        self.data["rssi.downlink"] = unpacked_data[7] * -1
        self.data["rssi.downlink.quality"] = unpacked_data[8]
        self.data["rssi.downlink.snr"] = unpacked_data[9]


    def parse_attitude(self, payload):
        if len(payload) != 6:
            print(f"Invalid payload length for Attitude: expected 6, got {len(payload)}")
            return
        pitch, roll, yaw = struct.unpack('>3h', payload)
        # Convert and store the data in the dictionary
        self.data["drone.pitch"] = pitch / 10000
        self.data["drone.roll"] = roll / 10000
        self.data["drone.yaw"] = yaw / 10000

        print(f"Pitch: {self.data['drone.pitch']}, Roll: {self.data['drone.roll']}, Yaw: {self.data['drone.yaw']}")

    
    def parse_flight_mode(self, payload):
        flight_mode = payload.decode('ascii').rstrip('\x00')
        # Store the data in the dictionary
        self.data["drone.flightmode"] = flight_mode

    @staticmethod
    def parse_ping_devices(_):
        return '[Ping Devices]'

    @staticmethod
    def parse_device(self, payload):
        return '[Device] 0x%02x "%s" %d parameters' % (payload[1], "".join([chr(c) for c in payload[2:-14]]), payload[-2])

    @staticmethod
    def parse_radio_id(payload):
        return '[RadioId] subcmd 0x%02x, interval %d, correction %d' % \
                (payload[2], int.from_bytes(payload[3:7], 'big')/10, int.from_bytes(payload[7:11], 'big', signed=True)/10)

    @staticmethod
    def parse_command(payload):
        if payload[2]==0x10 and payload[3]==5:
            return '[Command] subcmd 0x10,0x05, set ModelId, data %d' % (payload[4])
        return '[Command] subcmd 0x%02x, datatype 0x%02x, data %d' % \
                (payload[2], payload[3], payload[4])

    @staticmethod
    def parse_fields_request(payload):
        return '[Field request] device=0x%02x field=%d chunk=%d' % (payload[1], payload[2], payload[3])

    @staticmethod
    def parse_field_update(payload):
        return '[Field update] device=0x%02x field=%d' % (payload[1], payload[2])

    @staticmethod
    def parse_elrs_info(payload):
        return '[ELRS info] device=0x%02x bad=%d, good=%d, flags=0x%02x, flag_str=%s' % (payload[1], payload[2],
                int.from_bytes(payload[3:5], 'big'), payload[5], ''.join(map(chr, payload[6:-2])))


    def send_to_udp(self):
        for key in self.data:
            timestamp = time.time()
            message = "{},{},{}".format(key, self.data[key], timestamp)
            self.sock.sendto(message.encode(), (self.udp_ip, self.udp_port))
            # print(message)  # Optional debug print


    
 

if __name__ == "__main__":
    telemetry = DroneTelemetry()
    telemetry.process_serial_data()





