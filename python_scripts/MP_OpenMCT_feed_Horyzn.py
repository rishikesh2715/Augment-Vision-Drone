## same as MP_OpenMCT_feed, just with the variables implemented for Horyzn

import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 50013
MESSAGE = "23,567,32,4356,456,132,4353467"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

i = 0

try:
    while True:
        # Little counter to check for concurrency
        if i == 1000:
            i = 0
        else:
            i += 1

        ## add/uncomment desired values
        roll = cs.roll
        pitch = cs.pitch
        yaw = cs.yaw
        #desired attitude
        nav_roll = cs.nav_roll
        nav_pitch = cs.nav_pitch
        #latVal = cs.lat
        #lngVal = cs.lng
        groundcourse = cs.groundcourse
        alt = cs.alt
        #altoffsethomeVal = cs.altoffsethome
        #gpsstatus = cs.gpsstatus
        #gpshdopVal = cs.gpshdop
        satcount = cs.satcount
        #altd100Val = cs.altd100
        #altd1000Val = cs.altd1000
        airspeed = cs.airspeed
        tar_airspeed = cs.targetairspeed
        groundspeed = cs.groundspeed
        #verticalspeedVal = cs.verticalspeed
        wind_dir = cs.wind_dir
        wind_vel = cs.wind_vel
        ax = cs.ax
        ay = cs.ay
        az = cs.az
        #gxVal = cs.gx
        #gyVal = cs.gy
        #gzVal = cs.gz
        ### Servo Channels Input
        # chx1inVal = cs.chx1in
        # chx2inVal = cs.chx2in
        # chx3inVal = cs.chx3in
        # chx4inVal = cs.chx4in
        # chx5inVal = cs.chx5in
        # chx6inVal = cs.chx6in
        # chx7inVal = cs.chx7in
        # chx8inVal = cs.chx8in
        ### Servo Channels Output
        # chx1outVal = cs.chx1out
        # chx2outVal = cs.chx2out
        # chx3outVal = cs.chx3out
        # chx4outVal = cs.chx4out
        # chx5outVal = cs.chx5out
        # chx6outVal = cs.chx6out
        # chx7outVal = cs.chx7out
        # chx8outVal = cs.chx8ou
        #magnetic field param
        mx = cs.mx
        my = cs.my
        mz = cs.mz
        battV = cs.battery_voltage
        lidar_alt = cs.sonarrange
        radius = cs.radius
        climbrate = cs.climbrate
        turnrate = cs.turnrate
        distTraveled = cs.distTraveled

        timeStamp = time.time()

        # Build a message, add new curly bracket and variable name
        MESSAGE = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(roll, pitch, yaw, nav_roll, nav_pitch, groundcourse, alt, satcount, airspeed, tar_airspeed,groundspeed,wind_dir, wind_vel, ax, ay, az, mx, my, mz, battV, lidar_alt,radius,climbrate, turnrate, distTraveled)
        # Show the timestep
        print(MESSAGE)
        print('\n')

        # Pumping out the values
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Over")
