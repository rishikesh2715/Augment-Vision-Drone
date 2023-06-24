# example implementation of how to handle commands from the openmct telemetry server

import socket

UDP_IP = "127.0.0.1" #standard ip udp
UDP_PORT_IN = 60012 #chosen port from OpenMCT (same as in telemetry server object)

# initiate socket for rceiving and send first message
sockIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP

sockIn.bind((UDP_IP, UDP_PORT_IN))

while True:
    command = sockIn.recv(1024)
    #do sth with your command
    if command == b':exampleCommandtoPlane':
        #send comd via serial/MQTT/MissionPlanner
        print(command)
    else:
        print('unknown command!')
