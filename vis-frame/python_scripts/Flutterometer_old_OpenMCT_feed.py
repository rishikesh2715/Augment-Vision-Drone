# first implementation of the Flutterometer /FLIPASED communication
# now done with thibaults server
# in here as an example for parasing data from a serial port

import socket
import sys
import serial
import struct
import numpy as np


UDP_IP = "127.0.0.1" #standard ip udp
UDP_PORT = 50011 #chosen port to OpenMCT
MESSAGE = "" #init message

# which com port
comPort = sys.argv[1]
baudrate = 57600
array=[]



#init serial connection to telemetry module
ser = serial.Serial(comPort, baudrate, timeout=30)
print(ser.name)

# initiate socket and send first message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
except:
    print('Initial message failed!')


i = 0
run = True
while run:
    try:
        
        # get your data
        myByte = ser.read(1)  # Just reading one byte

        if myByte == b's':  # Since we are getting bytes, we have to use the byte representation
            print('start, length:')
            size = struct.unpack('hhh', ser.read(6))
            print(size)
            payload = ser.read(size[2])
            myByte = ser.read(1)
	    #print(np.frombuffer(payload)

            if myByte == b'e':
                #end byte received, decode payload
                array = np.frombuffer(payload)
                #print(array)
                for i in range(size[0]*size[1]-1):
                    MESSAGE = MESSAGE + '{},'.format(array[i])
                MESSAGE = MESSAGE + '{},'.format(array[size[0]*size[1]-1])

                #MESSAGE = strMessage.format(array[1],array[2],array[3], array[5],array[6],array[7],array[9],array[10],array[11], array[0])
                #MESSAGE = "{},{},{},{},{},{},{},{},{},{}".format(array[1],array[2],array[3], array[5],array[6],array[7],array[9],array[10],array[11], array[0])

     
        if i == 1000:
            i = 0
        else:
            i += 1
            
        # Message for OpenMCT must be the same structure as on the receiving side (telemetrysource)
        # especially timestamp needs to be at the same position
        

        # Pumping out the values
        sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
          

        #print and reset your message for validation and wait for the next loop 
        print(MESSAGE)
        print('\n')
        MESSAGE = ''
        
         
        #time.sleep(0.5)

        
        
    
    except:
        print('Nope, try again!')
        run = False
            
