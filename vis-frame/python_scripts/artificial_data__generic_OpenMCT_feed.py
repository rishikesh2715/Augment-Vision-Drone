## Minimalistic script to feed artificial data to a OpenMCT Telemetry Server 

import socket
import time
import random



UDP_IP = "127.0.0.1" # localhost address
UDP_PORT = 50012 # the UDP Port specified in your telemetry server object 
MESSAGE = "23,567,32,4356,456,132,4353467" #testmessage

# initiate socket and send first message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
except:
    print('Initial message failed!')

# keys (must be consisten with your keys in openMCT)
keys = [
    'key.1',
    'key.2',
    'key.3',
    'key.4',
]

i = 0
while True:
        start = time.time()

        if i == 1000:
            i = 0
        else:
            i += 1

        timeStamp = time.time()
        # Build and send a message (depends on how you handle it in yout server.on(message) in yout telemetry object)
        
        # Either with the keys (e.g. DG800, works great with MQTT Protocol (MQTT_OpenMCT_feed.py))
        for k in keys:
            MESSAGE = "{},{},{}".format(k, i , timeStamp)
            # Pumping out the values
            sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

        # or all the data in one message, no keys (e.g. from MP_OpenMCT_feed.py)
        # MESSAGE = "{},{},{},{},{},{},{},{},{}".format(data1,data2,data3,data1,data2,data3,data1,data2,timeStamp)
        # Pumping out the values
        #sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))


            print(MESSAGE)
            print('\n')

        time.sleep(0.100)

