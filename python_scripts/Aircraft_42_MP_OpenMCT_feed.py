# Data provider for the Aircraft_42 implementation
# Grabs Data from Mission Planner
# sends data to a specified UDP port
# Threading implemented to support the sending of commands without blocking the data forwarding to the OpenMCT Telemetry Server
# in this stage not inteded to be used on a real aircraft, only simulation. Threading and usage of sockets need to be improved

import socket
import time
import threading


UDP_IP = "127.0.0.1" #standard ip udp (localhost)


def sendToMCT(run):

    UDP_PORT_SEND =50016   #chosen port to OpenMCT (same as in telemetry server object)
    MESSAGE = "23,567,32,4356,456,132,4353467" #init message


    # initiate socket and send first message
    sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    try:
        sockSend.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT_SEND))
    except:
        print('Initial message failed!')

    while True:

        #choose your values (more available, check MP documentation https://ardupilot.org/planner/docs/using-python-scripts-in-mission-planner.html)
        data = {
        "rollVal" : cs.roll,
        "pitchVal" : cs.pitch,
        "yawVal" : cs.yaw,
        "latVal" : cs.lat,
        "lngVal" : cs.lng,
        "heading" : cs.groundcourse,
        "altVal" : cs.alt,
        #"altoffsethomeVal" : cs.altoffsethome,
        "gpsstatusVal" : cs.gpsstatus,
        #"gpshdopVal" : cs.gpshdop,
        #"satcountVal" : cs.satcount,
        #"altd100Val" : cs.altd100,
        #"altd1000Val" : cs.altd1000,
        "airspeedVal" : cs.airspeed,
        #"targetairspeedVal" : cs.targetairspeed,
        "groundspeedVal" : cs.groundspeed,
        #"verticalspeedVal" : cs.verticalspeed,
        #"wind_dirVal" : cs.wind_dir,
        #"wind_velVal" : cs.wind_vel,
        #"axVal" : cs.ax,
        #"ayVal" : cs.ay,
        "azVal" : -cs.az/1000,
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
            
            #print(MESSAGE)
            #print('\n')

            # Pumping out the values
            sockSend.sendto(MESSAGE, (UDP_IP, UDP_PORT_SEND))

            #print your message for validation and wait for the next loop
            #print(MESSAGE)
                    
        

        # Message for OpenMCT must be the same structure as on the receiving side (telemetrysource)
        # default is: key, value, timestamp in s UDP epoch time
        time.sleep(0.05)
        
        if not(run()): #to kill the thread
            print('Message Pump Closed!')
            break
            


def command(run):

    UDP_PORT_RCV = 50017   #chosen port to OpenMCT (same as in telemetry server object)
    data = ''
    addr = ''
    connected = False

    # initiate socket and send first message
    sockRcv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    try:
        sockRcv.bind((UDP_IP, UDP_PORT_RCV)) # bind the socket to the specified ip and port
        sockRcv.setblocking(0) # set the socket on unblocking, so we wont get stuck on sockRcv.recvfrom()
        connected = True # if connected go into the loop
    except:
        print('Connecting to Telemetry Server failed! Wait a couple of seconds, so the socket will close. Then restart the script.')
        sockRcv.close() # if connection fails retry
        

    while connected:
        try:
            data, address = sockRcv.recvfrom(1024) # buffer size is 1024 bytes
            print("received message: %s" % data)
        except socket.error:
            pass
        else:
            if data == ':dutchRoll':

                Script.ChangeMode('FBWB') # FBWB Flight mode Roll and pitch follow stick input, automatic height and speed control
                Script.SendRC(4,2000,True) # Rudder full deflection 
                Script.Sleep(500) #wait 500ms
                Script.SendRC(4,1000,True) # Rudder full deflection other direction
                Script.Sleep(500) #wait 500ms
                Script.SendRC(4,1500,True) # no rudder deflection
                Script.Sleep(5000) # wait 5s to let the aircraft oscillate
                Script.ChangeMode('Auto') # back to mode auto
                print('Dutch Roll finished!')
    
    
        if not(run()): #to kill the thread
            sockRcv.close()
            print('Command Closed!')
            break

    
#set the run argument true
run = True

# start the threads
sendMsgfromMP = threading.Thread(target=sendToMCT,args=(lambda : run, ))
sendMsgfromMP.start()

command = threading.Thread(target=command,args=(lambda : run, ))
command.start()



while True:
    try: #keep the main thread alive
        time.sleep(1)
    except: # on closing the main thread also close the function threads
        run=False 
        sendMsgfromMP.join()
        command.join()
        print('Ended!')

        



