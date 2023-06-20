import serial
import sys
import numpy as np
import time
import struct
import random
from message_parser import parser
from message_parser import initalizeParser
from checksum_calculator import calcChecksum
from command_message import getCommandMsg
from OpenMCT_send import sendtoOMCT

from bitarray import bitarray

# which com port
comPort = '/dev/ttyUSB1'
baudrate = 57600

cmdID = 23
StatusFlags = '1' 
Battery = '1'
XSens = '1' 
ADS = '1' 
PPM = '1'
DD = '0' #does not get parsed atm was not implemented in EDL as well
ECU = '1'
ServoRef = '1'
IMU_1 = '11111111' # Analog Acc Z / GyroX / Gyro Y / Digital Acc Z / IMU1 ...IMU4
IMU_2 = '11111111' # IMU5...IMU12
SHM_1 = '11111111' # Position / Temp / SHM1 ... SHM6
SHM_2 = '11111111' # SHM7 ... SHM14

# Get number of variables and number of IMUS/SHM
IMU_noVar = 0
for i in IMU_1[0:4]:
    if i == '1':
        IMU_noVar = IMU_noVar +1    
IMU_noIMU = 0
for i in IMU_1[4:]:
    if i == '1':
        IMU_noIMU = IMU_noIMU +1
for i in IMU_2:
    if i == '1':
        IMU_noIMU = IMU_noIMU +1

SHM_noVar = 0
for i in SHM_1[0:2]:
    if i == '1':
        SHM_noVar = SHM_noVar +1    
SHM_noSHM = 0
for i in SHM_1[2:]:
    if i == '1':
        SHM_noSHM = SHM_noSHM +1
for i in SHM_2:
    if i == '1':
        SHM_noSHM = SHM_noSHM +1

initalizeParser(StatusFlags, Battery, XSens, ADS, PPM, DD, ECU, ServoRef, IMU_1, IMU_2, SHM_1, SHM_2)

IDs = { #IDs with corresponding message length
    0 : 16, #ErrorFlag: ID:0, payload length: 1
    7 : 10, #Battery
    14: 67, #XSENS
    21: 18, #ADS: ID:21, payload length:18
    28: 34, #PPM
    35: 1, #DD
    42: 28, #ECU
    49: 44, #SERVO_REF
    56: IMU_noVar*IMU_noIMU*2 + 2, #IMU
    63: SHM_noVar*SHM_noSHM*2 + 2 #SHM
}
#print(IMU_noVar*IMU_noIMU*2 + 2)

#init serial connection to telemetry module
ser = serial.Serial(comPort, baudrate, timeout=30)
print(ser.name)

CommandMessage = getCommandMsg(cmdID, StatusFlags, Battery, XSens, ADS, PPM, DD, ECU, ServoRef, IMU_1, IMU_2, SHM_1, SHM_2)

print(CommandMessage)
for i in range(100):
    #ser.write(CommandMessage)
    time.sleep(0.01)

count = 0
pckg = 0
while True:
    #try:
        if count > 500:
            #resending of commandMsg for a more stable connection (according to EDL)
            #ser.write(CommandMessage)
            count = 0
            #print(str(CommandMessage) + ' requested')
        count = count + 1   
        x=0
        variableBits=''
        z = ser.read(1)
        checksum = 0
        h = struct.unpack('B', z)[0]
        payload = ()
        #print(h)
        if h == 150:
            #print('catched!')

            configID = struct.unpack('B', ser.read(1))[0]
            #print('Config ID: ' + str(ConfigID))
            msgID = struct.unpack('B', ser.read(1))[0]
            #print('Msg ID: ' + str(MsgID))
            
            try:
                for i in range(IDs[msgID]):
                    variableBits = variableBits+'B'
                    #print(variableBits)
            
                payload = struct.unpack(variableBits, ser.read(IDs[msgID]))
                #print(payload)
            except:
                 print('unknown Key: '+str(msgID)) 
                
            check = ser.read(1)
            head_payload = (150,configID,msgID)+payload
            #if msgID == 63: #to check raw payload of a specific payload (ID see id dicrtinary)
                #print(head_payload)
  
            if calcChecksum(head_payload):
                payload = np.array(payload,dtype=np.uint8)
                data = parser(IMU_noVar, IMU_noIMU, SHM_noVar, SHM_noSHM, IMU_1, SHM_1, msgID, payload)
                #print(data)
                sendtoOMCT(data, time.time())
                pckg = pckg +1
                print(pckg)

            
                
    #except:
        #print('fail!')         