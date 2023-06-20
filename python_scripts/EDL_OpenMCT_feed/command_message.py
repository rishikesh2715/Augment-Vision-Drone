import numpy as np



def getCommandMsg(CmdID, StatusFlags, Battery, XSens, ADS, PPM, DD, ECU, ServoRef, IMU_1, IMU_2, SHM_1, SHM_2):

    OnOffBits = StatusFlags + Battery + XSens + ADS + PPM + DD + ECU + ServoRef
    OnOffInt = int(OnOffBits,2)
        
    
    configId = CmdID #configuration identifier for flight head

    header = np.array([0,0], dtype=np.uint8)
    commandMessage = np.array(5, dtype=np.uint8)
    footer = 0#np.uint8(1)
    message = np.zeros(8, dtype=np.uint8)


    head_fix = '96'
    header[0] = (np.uint8(int(head_fix, 16)))
    header[1] = (np.uint8(configId))
    #print(header)
    
    commandMessage = [OnOffInt, int(IMU_1,2), int(IMU_2,2), int(SHM_1,2), int(SHM_2,2)]

    message[0:2] = header
    message[2:7] = commandMessage
    
    for part in message[0:7]:
        footer = np.uint8(np.bitwise_xor(footer,part))
        
    #print(footer)
    
    message[7] = footer

    return(message)
