# Example implementation on how to get (additional) data from MissionPlanner into OpenMCT

import socket
import time

UDP_IP = "127.0.0.1" #localhost
UDP_PORT = 50015 # your telemetry Object port
MESSAGE = "23,567,32,4356,456,132,4353467" # random test message

# initiate socket and send first message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
except:
    print('Initial message failed!')

i = 0
try:
    while True:
        # Counter to check for concurrency
        # if i == 1000:
        #     i = 0
        # else:
        #     i += 1

        #choose your values (more available, check MP documentation https://ardupilot.org/planner/docs/using-python-scripts-in-mission-planner.html)
        data = {
        "rollVal" : cs.roll,
        "pitchVal" : cs.pitch,
        #"yawVal" : cs.yaw,
        "latVal" : cs.lat,
        "lngVal" : cs.lng,
        "heading" : cs.groundcourse,
        "altVal" : cs.alt,
        #"altoffsethomeVal" : cs.altoffsethome,
        "gpsstatusVal" : cs.gpsstatus,
        #"gpshdopVal" : cs.gpshdop,
        #"satcountVal" : cs.satcount,
        #"altd100Val" : cs.altd100,
        "altd1000Val" : cs.altd1000,
        "airspeedVal" : cs.airspeed,
        #"targetairspeedVal" : cs.targetairspeed,
        "groundspeedVal" : cs.groundspeed,
        #"verticalspeedVal" : cs.verticalspeed,
        #"wind_dirVal" : cs.wind_dir,
        #"wind_velVal" : cs.wind_vel,
        "axVal" : cs.ax,
        "ayVal" : cs.ay,
        "azVal" : cs.az,
        #"gxVal" : cs.gx,
        #"gyVal" : cs.gy,
        #"gzVal" : cs.gz,
        ### Servo Channels Input
        # "chx1inVal" : cs.chx1in,
        # "chx2inVal" : cs.chx2in,
        # "chx3inVal" : cs.chx3in,
        # "chx4inVal" : cs.chx4in,
        # "chx5inVal" : cs.chx5in,
        # "chx6inVal" : cs.chx6in,
        # "chx7inVal" : cs.chx7in,
        # "chx8inVal" : cs.chx8in,
        ### Servo Channels Output
        # "chx1outVal" : cs.chx1out,
        # "chx2outVal" : cs.chx2out,
        # "chx3outVal" : cs.chx3out,
        # "chx4outVal" : cs.chx4out,
        # "chx5outVal" : cs.chx5out,
        # "chx6outVal" : cs.chx6out,
        # "chx7outVal" : cs.chx7out,
        # "chx8outVal" : cs.chx8out,
        "battery_voltageVal" : cs.battery_voltage,
        "battery_remainingVal" : cs.battery_remaining,
        "armed" : cs.armed

        }

        timeStamp = time.time()
        for key, value in data.items():
            MESSAGE = "{},{},{}".format(key, value, timeStamp)
            
            print(MESSAGE)
            print('\n')

            # Pumping out the values
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            time.sleep(0.01)

except KeyboardInterrupt:
    print("Over")
