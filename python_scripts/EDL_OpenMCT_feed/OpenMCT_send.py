import socket

UDP_IP = "127.0.0.1" #standard ip udp
UDP_PORT = 50011 #chosen port to OpenMCT
MESSAGE = "" #init message

# initiate socket and send first message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
try:
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
except:
    print('Initial message failed!')


def sendtoOMCT(data,timestamp):
    #try:
        datapoints = len(data)/2
        count = 0
        #print("sendin")
        for i in range(int(datapoints)):
            MESSAGE = '{},{},{}'.format(data[count],data[count+1],timestamp)
            count = count +2
            # Pumping out the values

            sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

            #print and reset your message for validation and wait for the next loop 
            #print(MESSAGE)
            #print('\n')
            #MESSAGE = ''        
            
            #time.sleep(0.5)

    # except:
    #     #print('Nope, try again!')
    #     return(True)
            
