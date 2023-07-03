# Artificial Data provider for the DG800 MQTT implementation
# sends artificial data to an specified UDP port

import socket
import time


UDP_IP = "127.0.0.1" #standard ip udp
UDP_PORT = 50012 #chosen port to OpenMCT (same as in telemetry server object)
MESSAGE = "23,567,32,4356,456,132,4353467" #init message

data = 0 #artificial data

topics = [
    # those are the keys for the DG800, which are declared in the dictionary on OpenMCT side
    # since they are not sent, we have ti initialize them here
        "data.gps.iTOW",
        "data.gps.lon",
        "data.gps.lat" ,
        "data.gps.heightMS" ,
        "data.gps.gSpeed",
        "data.gps.headingMotion" ,
        "data.gps.headingVehicle" ,
		"data.gps.fixType" ,

        "data.nano.vdot" ,
        "data.nano.v" ,
		"data.nano.ch1" ,
		"data.nano.ch2" ,
		"data.nano.ch3" ,
		"data.nano.ch4" ,
		"data.nano.ch5" ,
		"data.nano.ch6" ,
		"data.nano.ch7" ,
		"data.nano.ch8" ,
		"data.nano.ch9" ,
		"data.nano.ch10" ,
		"data.nano.ch11" ,
		"data.nano.ch12" ,
		"data.nano.ch13" ,

        "data.strap.roll",
        "data.strap.pitch" ,
        "data.strap.yaw" ,

        "data.thr.force1" ,
        "data.thr.force2" ,
		"data.thr.temp1" ,
		"data.thr.temp2" ,

		"data.imu.AccX" ,
		"data.imu.AccY" ,
		"data.imu.AccZ" ,
		"data.imu.GyroX" ,
		"data.imu.GyroY" ,
		"data.imu.GyroZ" ,

		"data.adp.pstat" ,
		"data.adp.pdyn" ,
		"data.adp.AirSpeed"

]

#print(len(topics))

# initiate socket and send first message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
except:
    print('Initial message failed!')

# initial positional values
lon = 11.273738
lat = 48.069299
hdg = 0

while True:

    for i in range(len(topics)):
        
        # a little logic to create "meaningful" poitional data (Map Plugin testing)
        if topics[i]=="data.gps.lon":
            if lon >= 11.296338:
                lon = 11.273738
            timeStamp = time.time()
            MESSAGE = "{},{},{}".format(topics[i],lon,timeStamp)
            sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
            lon = lon + 0.000062778
            continue
        
        if topics[i]=="data.gps.lat":
            if lat >= 48.069299+0.0226:
                lat = 48.069299
            timeStamp = time.time()
            MESSAGE = "{},{},{}".format(topics[i],lat,timeStamp)
            sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
            lat = lat + 0.000062778
            continue

        if topics[i]=="data.gps.headingMotion":
            if hdg == 360:
                hdg = 0
            timeStamp = time.time()
            MESSAGE = "{},{},{}".format(topics[i],hdg,timeStamp)
            sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
            hdg = hdg + 1
            continue

        timeStamp = time.time()
        #built message
        MESSAGE = "{},{},{}".format(topics[i],data+i,timeStamp)
        # Pumping out the values
        sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

        #print your message for validation and wait for the next loop
        #print(MESSAGE)
                
    # all data goes from 0 to 1000 and then resets
    if data < 1000:
        data = data + 1
    else:
        data = 0
    print(data)

    # Message for OpenMCT must be the same structure as on the receiving side (telemetrysource)
    # especially timestamp needs to be at the same position
    # for simulation of DG800 Bandwith, 40 Values at ca. 10Hz -> 400Hz
    time.sleep(0.005) #considering time needed by python script
