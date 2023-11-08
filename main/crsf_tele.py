import serial
import struct
from serial import Serial

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

class Drone:
    def __init__(self):
        self.lat = None
        self.lon = None
        self.speed = None
        self.heading = None
        self.altitude = None
        self.sats = None
        self.pitch = None
        self.roll = None
        self.yaw = None

class CRSFParser:
    RADIO_ADDRESS = 0xea
    FRAME_TYPES = {
        0x02: "ParseGPS",
        0x08: "ParseBattery",
        0x10: "ParseVtxTelem",
        0x14: "ParseLinkStatistics",
        0x16: "ParseChannels",
        0x1E: "ParseAttitude",
        0x21: "ParseFlightMode",
        0x28: "ParsePingDevices",
        0x29: "ParseDevice",
        0x2a: "ParseFieldsRequest",
        0x2b: "ParseField",
        0x2c: "ParseFieldRequest",
        0x2d: "ParseFieldUpdate",
        0x2e: "ParseELRSInfo",
        0x32: "ParseCommand",
        0x3a: "ParseRadioId",
    }


    def __init__(self, port='COM7', baudrate=115200):
        self.ser = serial.Serial(port, baudrate)
        if not self.ser.is_open:
            self.ser.open()
        self.drone = Drone()

    def processSerialData(self):
        while True:
            device_address = self.ser.read(1)
            if ord(device_address) == self.RADIO_ADDRESS:
                self.parsePacket()
            else:
                print(f'Unknown device address: {device_address}')

    def parsePacket(self):
        frame_length = struct.unpack('<B', self.ser.read(1))[0]
        frame_type = struct.unpack('<B', self.ser.read(1))[0]
        payload = self.ser.read(frame_length - 2)
        crc = struct.unpack('<B', self.ser.read(1))[0]
        calculated_crc = self.crc8_dvb_s2(bytes([frame_type]) + payload)
        if calculated_crc != crc:
            print("CRC error: calculated CRC does not match received CRC. Data may be corrupted.")
        else:
            self.parsePayload(frame_type, payload)

    def parsePayload(self, frame_type, payload):
        if frame_type in self.FRAME_TYPES:
            method_name = self.FRAME_TYPES[frame_type]
            method = getattr(self, method_name, lambda x: "Invalid frame type")
            method(payload)
        else:
            print(f'Unknown frame type: {frame_type}')

    def ParseGPS(self, payload):
        lat, lon, speed, heading, altitude, sats = struct.unpack('>iiHHHB', payload)
        self.drone.lat = lat / 1e7
        self.drone.lon = lon / 1e7
        self.drone.speed = speed / 100
        self.drone.heading = heading / 100
        self.drone.altitude = altitude - 1000
        self.drone.sats = sats

    def ParseBattery(self, payload):
        voltage = float((payload[0] << 8) + payload[1]) / 10
        current = float((payload[2] << 8) + payload[3]) / 10
        consumption = (payload[4] << 16) + (payload[5] << 8) + payload[6]
        return "[Battery] %.1fV %.1fA %dmAh" % (voltage, current, consumption)

    def ParseVtxTelem(self, payload):
        return "[VTX Telemetry] freq=%d, power=%d, pitmode=%d" % (int.from_bytes(payload[1:3], 'big'), int(payload[3]), int(payload[4]))

    def ParseLinkStatistics(self, payload):
        return "[Link Statistics] "

    def ParseChannels(self, payload):
        return "[Channel Data] "

    def ParseAttitude(self, payload):
        if len(payload) != 6:
            print("Invalid payload length for Attitude: expected 6, got {len(payload)}")
            return
        
        #convert to signed shorts (-32768 to 32767)
        pitch, roll, yaw = struct.unpack('>3h', payload)
        # Assuming payload is a list or tuple of byte values
        pitch = float(pitch) / 10000
        roll = float(roll) / 10000
        yaw = float(yaw) / 10000

        # formatted pitch, roll, and yaw values to print with 3 decimal places
        attitude_str = "[Attitude] pitch=%.3f roll=%.3f yaw=%.3f" % (pitch, roll, yaw)
        
        # Print the attitude string
        print(attitude_str)
        
        # returning the attitude string for openMCT
        return attitude_str
    
    def ParseFlightMode(self, payload):
        return '[Flight Mode] "%s"' % "".join([chr(c) for c in payload[:-1]])

    def ParsePingDevices(_):
        return '[Ping Devices]'

    def ParseDevice(self, payload):
        return '[Device] 0x%02x "%s" %d parameters' % (payload[1], "".join([chr(c) for c in payload[2:-14]]), payload[-2])

    def ParseRadioId(self, payload):
        return '[RadioId] subcmd 0x%02x, interval %d, correction %d' % \
                (payload[2], int.from_bytes(payload[3:7], 'big')/10, int.from_bytes(payload[7:11], 'big', signed=True)/10)

    def ParseCommand(self, payload):
        if payload[2]==0x10 and payload[3]==5:
            return '[Command] subcmd 0x10,0x05, set ModelId, data %d' % (payload[4])
        return '[Command] subcmd 0x%02x, datatype 0x%02x, data %d' % \
                (payload[2], payload[3], payload[4])

    def ParseFieldsRequest(self, payload):
        return '[Fields request]'

    def ParseFieldRequest(self, payload):
        return '[Field request] device=0x%02x field=%d chunk=%d' % (payload[1], payload[2], payload[3])

    def ParseFieldUpdate(self, payload):
        return '[Field update] device=0x%02x field=%d' % (payload[1], payload[2])

    def ParseELRSInfo(self, payload):
        return '[ELRS info] device=0x%02x bad=%d, good=%d, flags=0x%02x, flag_str=%s' % (payload[1], payload[2],
                int.from_bytes(payload[3:5], 'big'), payload[5], ''.join(map(chr, payload[6:-2])))
        

    def crc8_dvb_s2(self, data):
        crc = 0
        for byte in data:
            crc = crc8_dvb_s2_table[crc ^ byte] 
        return crc

if __name__ == "__main__":
    parser = CRSFParser()
    parser.processSerialData()







