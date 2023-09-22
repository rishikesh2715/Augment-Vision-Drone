# coding:UTF-8
"""
    Test File
"""
import time
import datetime
import platform
import struct
import lib.device_model as deviceModel
import math
from lib.data_processor.roles.jy901s_dataProcessor import JY901SDataProcessor
from lib.protocol_resolver.roles.wit_protocol_resolver import WitProtocolResolver
import multiprocessing

welcome = """
Welcome to the Wit-Motion sample program
"""
_writeF = None                    # File writing
_IsWriteF = False                 # File writing flag
pilot = {}
q = multiprocessing.Queue()

def readConfig(device):
    """
    Example of reading configuration information
    :param device: Device model
    :return:
    """
    tVals = device.readReg(0x02, 3)  # Read data content, return rate, communication rate
    if len(tVals) > 0:
        print("Return result: " + str(tVals))
    else:
        print("No return")
    tVals = device.readReg(0x23, 2)  # Read installation direction, algorithm
    if len(tVals) > 0:
        print("Return result: " + str(tVals))
    else:
        print("No return")

def setConfig(device):
    """
    Example setting configuration information
    :param device: Device model
    :return:
    """
    device.unlock()
    time.sleep(0.1)
    device.writeReg(0x03, 6)       # Set the transmission back rate to 10HZ
    time.sleep(0.1)
    device.writeReg(0x23, 0)       # Set installation direction: horizontal and vertical
    time.sleep(0.1)
    device.writeReg(0x24, 0)       # Set installation direction: nine-axis, six-axis
    time.sleep(0.1)
    device.save()

def AccelerationCalibration(device):
    """
    Acceleration calibration
    :param device: Device model
    :return:
    """
    device.AccelerationCalibration()
    print("Acceleration calibration completed")

def FiledCalibration(device):
    """
    Magnetic field calibration
    :param device: Device model
    :return:
    """
    device.BeginFiledCalibration()  # Start field calibration
    if input("Rotate slowly around the XYZ axis, after completing three-axis rotation, end calibration (Y/N)?").lower() == "y":
        device.EndFiledCalibration()  # End field calibration
        print("End magnetic field calibration")

def onUpdate(deviceModel):
    """
    Data update event
    :param deviceModel: Device model
    :return:
    """    
    
    # Calculate compass direction
    magX = deviceModel.getDeviceData("magX")
    magY = deviceModel.getDeviceData("magY")
    magZ = deviceModel.getDeviceData("magZ")

    # Calculate the azimuth angle (compass direction) in degrees
    azimuth_rad = math.atan2(magY, magX)
    azimuth_deg = math.degrees(azimuth_rad)

    # Ensure the azimuth is within the range [0, 360)
    compass_direction = (azimuth_deg + 360) % 360
    pilot.direction = compass_direction
    pilot.lat = deviceModel.getDeviceData("lat")
    pilot.lon = deviceModel.getDeviceData("lon") # pilot.long chnaged it to pilot.lon -- long is built-in function
    q.put(pilot)

    # print("Compass Direction:", compass_direction)
    # print("Chip time: " + str(deviceModel.getDeviceData("Chiptime"))
    #     , " Temperature: " + str(deviceModel.getDeviceData("temperature"))
    #     , " Acceleration: " + str(deviceModel.getDeviceData("accX")) + "," + str(deviceModel.getDeviceData("accY")) + "," + str(deviceModel.getDeviceData("accZ"))
    #     , " Angular velocity: " + str(deviceModel.getDeviceData("gyroX")) + "," + str(deviceModel.getDeviceData("gyroY")) + "," + str(deviceModel.getDeviceData("gyroZ"))
    #     , " Angles: " + str(deviceModel.getDeviceData("angleX")) + "," + str(deviceModel.getDeviceData("angleY")) + "," + str(deviceModel.getDeviceData("angleZ"))
    #     , " Magnetic field: " + str(deviceModel.getDeviceData("magX")) + "," + str(deviceModel.getDeviceData("magY")) + "," + str(deviceModel.getDeviceData("magZ"))
    #     , " Longitude: " + str(pilot.lon) + " Latitude: " + str(pilot.lat)
    #     , " Yaw: " + str(deviceModel.getDeviceData("Yaw")) + " Ground speed: " + str(deviceModel.getDeviceData("Speed"))
    #     , " Quaternions: " + str(deviceModel.getDeviceData("q1")) + "," + str(deviceModel.getDeviceData("q2")) + "," + str(deviceModel.getDeviceData("q3")) + "," + str(deviceModel.getDeviceData("q4"))
    # )
    if _IsWriteF:  # Record data
        Tempstr = " " + str(deviceModel.getDeviceData("Chiptime"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("accX")) + "\t" + str(deviceModel.getDeviceData("accY")) + "\t" + str(deviceModel.getDeviceData("accZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("gyroX")) + "\t" + str(deviceModel.getDeviceData("gyroY")) + "\t" + str(deviceModel.getDeviceData("gyroZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("angleX")) + "\t" + str(deviceModel.getDeviceData("angleY")) + "\t" + str(deviceModel.getDeviceData("angleZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("temperature"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("magX")) + "\t" + str(deviceModel.getDeviceData("magY")) + "\t" + str(deviceModel.getDeviceData("magZ"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("lon")) + "\t" + str(deviceModel.getDeviceData("lat"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("Yaw")) + "\t" + str(deviceModel.getDeviceData("Speed"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("q1")) + "\t" + str(deviceModel.getDeviceData("q2"))
        Tempstr += "\t" + str(deviceModel.getDeviceData("q3")) + "\t" + str(deviceModel.getDeviceData("q4"))
        Tempstr += "\r\n"
        _writeF.write(Tempstr)

# def startRecord():
#     """
#     Start recording data
#     :return:
#     """
#     global _writeF
#     global _IsWriteF
#     _writeF = open(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + ".txt", "w")  # Create a new file
#     _IsWriteF = True  # Mark as writable
#     Tempstr = "Chiptime"
#     Tempstr += "\tax(g)\tay(g)\taz(g)"
#     Tempstr += "\twx(deg/s)\twy(deg/s)\twz(deg/s)"
#     Tempstr += "\tAngleX(deg)\tAngleY(deg)\tAngleZ(deg)"
#     Tempstr += "\tT(°)"
#     Tempstr += "\tmagx\tmagy\tmagz"
#     Tempstr += "\tlon\tlat"
#     Tempstr += "\tYaw\tSpeed"
#     Tempstr += "\tq1\tq2\tq3\tq4"
#     Tempstr += "\r\n"
#     _writeF.write(Tempstr)
#     print("Start recording data")

# def endRecord():
#     """
#     End recording data
#     :return:
#     """
#     global _writeF
#     global _IsWriteF
#     _IsWriteF = False  # Mark as not writable
#     _writeF.close()  # Close file
#     print("End recording data")

def runScript(mainPilot, queue):
    try:
        global pilot, q
        pilot = mainPilot
        q = queue
        print("Starting GPS script:")

        print(welcome)
        """
        Initialize a device model
        """
        device = deviceModel.DeviceModel(
            "My JY901",
            WitProtocolResolver(),
            JY901SDataProcessor(),
            "51_0"
        )

        if platform.system().lower() == 'linux':
            device.serialConfig.portName = "/dev/ttyUSB0"   # Set serial port
        else:
            device.serialConfig.portName = "COM9"          # Set serial port
        device.serialConfig.baud = 9600                     # Set baud rate
        device.openDevice()                                 # Open serial port
        readConfig(device)                                  # Read configuration information
        device.dataProcessor.onVarChanged.append(onUpdate)  # Data update event

        # startRecord()                                       # Start recording data
        input()
        device.closeDevice()
        # endRecord()                                         # End recording data
    except EOFError:
        pass
