# Artificial Data provider for the Drone implementation
# sends artificial data to an specified UDP port

import socket
import time


UDP_IP = "127.0.0.1" #standard ip udp (localhost)
UDP_PORT =50020   #chosen port to OpenMCT (same as in telemetry server object)
MESSAGE = "23,567,32,4356,456,132,4353467" #init message

data = 0 #artificial data

keys = [
    # those are the keys for the Drone, which are declared in the dictionary on OpenMCT side
    # since they are not sent, we have ti initialize them here
        "gps.lat","key.1","key.2","key.3","key.4","key.5","key.6","key.7","key.8","key.9","key.10","key.11","key.12","key.13","key.14","key.15","key.16","key.17","key.18","key.19","key.20","key.21","key.22","key.23","key.24",

]

#print(len(topics))

data = 0

# initiate socket and send first message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
except:
    print('Initial message failed!')

while True:

    for i in range(len(keys)):
       
        timeStamp = time.time()
        #built message
        MESSAGE = "{},{},{}".format(keys[i],data+i,timeStamp)
        # Pumping out the values
        sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

        #print your message for validation and wait for the next loop
        print(MESSAGE)
                
    # all data goes from 0 to 1000 and then resets
    if data < 100:
        data = data + 1
    else:
        data = 0
    print(data)

    # Message for OpenMCT must be the same structure as on the receiving side (telemetrysource)
    time.sleep(0.1) 
