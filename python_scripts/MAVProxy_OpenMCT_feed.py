# communication via MavProxy UDP socket (alternative to MissionPlanner)
# needs to be adapted to work with the current telemetry source object of the telemetry server
# still in the repository as am example on handling the MAVLink protocol

from pymavlink import mavutil
import socket
import time

# gets data from a MAVProxy instance through a UDP Port
# example on a MavLink implementation
# can request specific data

def recv_match(self, condition=None, type=None, blocking=False, timeout=None):
    '''Receive the next MAVLink message that matches the given type and condition
    type:        Message name(s) as a string or list of strings - e.g. 'SYS_STATUS'
    condition:   Condition based on message values - e.g. 'SYS_STATUS.mode==2 and SYS_STATUS.nav_mode==4'
    blocking:    Set to wait until message arrives before method completes. 
    timeout:     ? <!-- timeout for blocking message when the system will return. Is this just a time? -->
    '''

UDP_IP = "127.0.0.1"
UDP_PORT = 50011
MESSAGE = "23,567,32,4356,456,132,4353467"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('udpin:localhost:14550')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_system))
time.sleep(2)
# Once connected, use 'the_connection' to get and send messages

i = 0
run = True
while run:
    try:
        
        ## wait for and intercept messages as they arrive
        GPS_i = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)  # Note, you can access message fields as attributes!
        GPS_raw = the_connection.recv_match(type='GPS_RAW_INT', blocking=True)
        Att = the_connection.recv_match(type='ATTITUDE', blocking=True)
        IMU = the_connection.recv_match(type='SCALED_IMU2', blocking=True)
        timeStamp = time.time()

        # epoch_time = time.time()
        # timestamp = time.ctime(epoch_time)
        # print('Velocity: ', GPS_raw.vel/100, 'm/s')
        # print('Altitude: ', GPS_i.relative_alt/1000, 'm')
        # print('Timestamp: ', timestamp)

        
        if i == 1000:
            i = 0
        else:
            i += 1
            
        # Message for OpenMCT
        MESSAGE = "{},{},{},{},{},{},{},{},{}".format(Att.pitch*180/3.1415926, Att.roll*180/3.1415926, GPS_raw.vel/100, GPS_i.relative_alt/1000, IMU.xacc/1000, IMU.yacc/1000, IMU.zacc/1000, i, timeStamp)
        #MESSAGE = "{},{},{},{},{},{}".format(Att.pitch*180/3.1415926, Att.roll*180/3.1415926, GPS_raw.vel/100, GPS_i.relative_alt/1000, i, timeStamp)

        # Pumping out the values
        sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
          
         
        print(MESSAGE)
        print('\n')
        # time.sleep(0.005)

        
        
    
    except:
        print('Nope, try again!')
        run = False
            
