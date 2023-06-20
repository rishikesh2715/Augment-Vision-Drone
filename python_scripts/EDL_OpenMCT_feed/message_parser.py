import numpy as np
import struct
from load_wing_config import getCoefficients

def initalizeParser(StatusFlags, Battery, XSens, ADS, PPM, DD, ECU, ServoRef, IMU_1, IMU_2, SHM_1, SHM_2):

    if StatusFlags[0] == '1': 
        global errFlag
        errFlag = [
                'Flag.RxMux1.Autopilot', 0,  #1
                'Flag.RxMux1.SPI', 0,         #3
                'Flag.RxMux1.ECU_PIN', 0,     #5
                'Flag.RxMux1.ECU_PPM', 0,     #7
                'Flag.RxMux1.JETI', 0,        #9
                'Flag.RxMux1.GRP', 0,         #11
                'Flag.RxMux1.c_JETI', 0,      #13
                'Flag.RxMux1.c_GRP', 0, #15

                'Flag.RxMux2.Autopilot', 0,  #17 
                'Flag.RxMux2.SPI', 0,         #19
                'Flag.RxMux2.ECU_PIN', 0,     #21
                'Flag.RxMux2.ECU_PPM', 0,     #23
                'Flag.RxMux2.JETI', 0,        #25
                'Flag.RxMux2.GRP', 0,         #27
                'Flag.RxMux2.c_JETI', 0,      #29
                'Flag.RxMux2.c_GRP', 0, #31

                'Flag.RxMux3.Autopilot', 0,   #33
                'Flag.RxMux3.SPI', 0,         #35
                'Flag.RxMux3.ECU_PIN', 0,     #37
                'Flag.RxMux3.ECU_PPM', 0,     #39
                'Flag.RxMux3.JETI', 0,        #41
                'Flag.RxMux3.GRP', 0,         #43
                'Flag.RxMux3.c_JETI', 0,      #45
                'Flag.RxMux3.c_GRP', 0,   #47

                'Flag.flightHAT.XsensConfigFault', 0,     #49   
                'Flag.flightHAT.XsensUnexpectedConfigAck', 0,    #51
                'Flag.flightHAT.XsensConfigChecksumFault', 0,    #53
                'Flag.flightHAT.XsensConfigReceiveFault', 0,     #55
                'Flag.flightHAT.XsensWrongHeader', 0,        #57
                'Flag.flightHAT.XsensChecksumFault', 0,      #59
                'Flag.flightHAT.XsensDataTypeError', 0,      #61
                'Flag.flightHAT.XsensUnexpectedByteIndex', 0,    #63
                'Flag.flightHAT.XsensUnexpectedDataID', 0,   #65
                'Flag.flightHAT.ADSConfigFault', 0,          #67
                'Flag.flightHAT.ADSChecksumFault', 0,        #69
                'Flag.flightHAT.ADSTooMuchDataTypes', 0,     #71
                'Flag.flightHAT.IMUWrongRequestID', 0,       #73
                'Flag.flightHAT.IMUWrongID', 0,              #75
                'Flag.flightHAT.SHMWrongID', 0,              #77
                'Flag.flightHAT.WrongRXMUXChecksum', 0   #79

        ]

    if Battery[0] == '1': 
        global bat
        bat = [
            "Bat.RX_MUX1", 0,
            "Bat.RX_MUX2", 0,
            "Bat.RX_MUX3", 0,
            "Bat.FlightHead", 0
        ]

    if XSens[0] == '1': 
        global xsens
        xsens = [
                'xSens.Hour',        np.uint8(0), #1
                'xSens.Minute',      np.uint8(0), #3
                'xSens.Second',      np.uint8(0), #5
                'xSens.Millisecond',np.uint16(0), #7
                'xSens.EulerA',          np.float32(0), #9
                'xSens.EulerB',          np.float32(0),#11
                'xSens.EulerY',          np.float32(0), #13
                'xSens.ECEFX',          np.float32(0),#15
                'xSens.ECEFY',          np.float32(0),#17
                'xSens.ECEFZ',          np.float32(0), #19
                'xSens.AngularVa',      np.float32(0),#21
                'xSens.AngularVb',      np.float32(0),#23
                'xSens.AngularVy',      np.float32(0), #25
                'xSens.AccX',         np.float32(0),#27
                'xSens.AccY',         np.float32(0),#29
                'xSens.AccZ',         np.float32(0), #31
                'xSens.VelX',             np.float32(0), #33
                'xSens.VelY',             np.float32(0), #35
                'xSens.Sec',            np.double(0), #37
                'xSens.Latency',        np.double(0) #39       
        ]  

    if ADS[0] == '1': 
        global ads
        ads = [
                'ads.altitude',        np.uint32(0),
                'ads.angleOfAttack',      np.uint32(0), 
                'ads.sideslip',      np.uint32(0), 
                'ads.velocity', np.uint32(0)
        ]
    if PPM[0] == '1': 
        global ppm
        ppm = [None] * 32
        count = 0
        for i in range(int(len(ppm)/2)):
            ppm[count] = 'ppm.ch'+str(i)
            count = count + 2 

    if DD[0] == '1': 
        global dd
        dd = [
        "dd.1", 0
        ]

    if ECU[0] == '1': 
        global ecu
        ecu = [
            'ecu.FuelFlowPerSec', 0, #1
            'ecu.PupmVoltage', 0, #3
            'ecu.RPMActual', 0, #5
            'ecu.RPMControl', 0, #7
            'ecu.Status', 0, #9
            'ecu.Temp', 0, #11
            'ecu.Throttle', 0 #13
        ]

    if ServoRef[0] == '1': 
        global servo_ref
        servo_ref = [None] * 42
        count = 0
        for i in range(int(len(servo_ref)/2)):
            servo_ref[count] = 'servo_rev.ID'+str(i)
            count = count + 2
        global PWM_coeff
        PWM_coeff = getCoefficients('PWM')
        

    global imu
    imu=[]
    if IMU_1[0] == '1':
        pos = 1
        for j in IMU_1[4:]:
            if j == '1':
                imu.extend(['imu'+str(pos)+'.AnlAccZ', 0])
            pos = pos +1
        pos = 5
        for j in IMU_2[:]:
            if j == '1':
                imu.extend(['imu'+str(pos)+'.AnlAccZ', 0])
            pos = pos +1

    if IMU_1[1] == '1':
        pos = 1
        for j in IMU_1[4:]:
            if j == '1':
                imu.extend(['imu'+str(pos)+'.GyroX', 0])
            pos = pos +1
        pos = 5
        for j in IMU_2[:]:
            if j == '1':
                imu.extend(['imu'+str(pos)+'.GyroX', 0])
            pos = pos +1

    if IMU_1[2] == '1':
        pos = 1
        for j in IMU_1[4:]:
            if j == '1':
                imu.extend(['imu'+str(pos)+'.GyroY', 0])
            pos = pos +1
        pos = 5
        for j in IMU_2[:]:
            if j == '1':
                imu.extend(['imu'+str(pos)+'.GyroY', 0])
            pos = pos +1

    if IMU_1[3] == '1':
        pos = 1
        for j in IMU_1[4:]:
            if j == '1':
                imu.extend(['imu'+str(pos)+'.DigAccZ', 0])
            pos = pos +1
        pos = 5
        for j in IMU_2[:]:
            if j == '1':
                imu.extend(['imu'+str(pos)+'.DigAccZ', 0])
            pos = pos +1
    #print(imu)

    global shm
    shm=[]
    if SHM_1[0] == '1':
        pos = 1
        for j in SHM_1[2:]:
            if j == '1':
                shm.extend(['shm'+str(pos)+'.Pos', 0])
            pos = pos + 1
        pos = 7
        for j in SHM_2[:]:
            if j == '1':
                shm.extend(['shm'+str(pos)+'.Pos', 0])
            pos = pos + 1

    if SHM_1[1] == '1':
        pos = 1
        for j in SHM_1[2:]:
            if j == '1':
                shm.extend(['shm'+str(pos)+'.Temp', 0])
            pos = pos +1
        pos = 7
        for j in SHM_2[:]:
            if j == '1':
                shm.extend(['shm'+str(pos)+'.Temp', 0])
            pos = pos +1
    global SHM_coeff
    SHM_coeff = getCoefficients('SHM')
    #print(shm)

def bitget(number, pos):
    return (number >> pos) & 1    


def parser(IMU_noVar, IMU_noIMU, SHM_noVar, SHM_noSHM, IMU_1, SHM_1, MsgID, payload):
    #print(str(msg)+'imported!')
    # define the function blocks

## ErrorFlag
    def errorFlag():
        #print(payload)
        flightHatU16 = np.ndarray((1,), buffer = payload[0:2], dtype=np.uint16)
        
        rx_mux1U16 = np.ndarray((1,), buffer = payload[2:4], dtype=np.uint16)
        rx_mux1TimeU16 = np.ndarray((1,), buffer = payload[4:6], dtype=np.uint16)

        rx_mux2U16 = np.ndarray((1,), buffer = payload[6:8], dtype=np.uint16)
        rx_mux2TimeU16 = np.ndarray((1,), buffer = payload[8:10], dtype=np.uint16)

        rx_mux3U16 = np.ndarray((1,), buffer = payload[10:12], dtype=np.uint16)
        rx_mux3TimeU16 = np.ndarray((1,), buffer = payload[12:14], dtype=np.uint16)

        errFlag[49] = bitget(flightHatU16,15)[0]
        errFlag[51] = bitget(flightHatU16,14)[0]
        errFlag[53] = bitget(flightHatU16,13)[0]
        errFlag[55] = bitget(flightHatU16,12)[0]
        errFlag[57] = bitget(flightHatU16,11)[0]
        errFlag[59] = bitget(flightHatU16,10)[0]
        errFlag[61] = bitget(flightHatU16,9)[0]
        errFlag[63] = bitget(flightHatU16,8)[0]
        errFlag[65] = bitget(flightHatU16,7)[0]
        errFlag[67] = bitget(flightHatU16,6)[0]
        errFlag[69] = bitget(flightHatU16,5)[0]
        errFlag[71] = bitget(flightHatU16,4)[0]
        errFlag[73] = bitget(flightHatU16,3)[0]
        errFlag[75] = bitget(flightHatU16,2)[0]
        errFlag[77] = bitget(flightHatU16,1)[0]
        errFlag[79] = bitget(flightHatU16,0)[0]

        errFlag[1] = bitget(rx_mux1U16,0)[0]
        errFlag[2] = bitget(rx_mux1U16,1)[0]
        errFlag[5] = bitget(rx_mux1U16,2)[0]
        errFlag[7] = bitget(rx_mux1U16,3)[0]
        errFlag[9] = bitget(rx_mux1U16,4)[0]
        errFlag[11] = bitget(rx_mux1U16,5)[0]
        errFlag[13] = bitget(rx_mux1U16,6)[0]
        errFlag[15] = bitget(rx_mux1U16,7)[0]
        # Bit 8: DD1,
        # Bit 9: DD2,
        # Bit 10: Chute
        # Bit 11-15: Unused

        errFlag[17] = bitget(rx_mux2U16,0)[0]
        errFlag[19] = bitget(rx_mux2U16,1)[0]
        errFlag[21] = bitget(rx_mux2U16,2)[0]
        errFlag[23] = bitget(rx_mux2U16,3)[0]
        errFlag[25] = bitget(rx_mux2U16,4)[0]
        errFlag[27] = bitget(rx_mux2U16,5)[0]
        errFlag[29] = bitget(rx_mux2U16,6)[0]

        errFlag[33] = bitget(rx_mux3U16,0)[0]
        errFlag[35] = bitget(rx_mux3U16,1)[0]
        errFlag[37] = bitget(rx_mux3U16,2)[0]
        errFlag[39] = bitget(rx_mux3U16,3)[0]
        errFlag[41] = bitget(rx_mux3U16,4)[0]
        errFlag[43] = bitget(rx_mux3U16,5)[0]
        errFlag[45] = bitget(rx_mux3U16,6)[0]
        errFlag[47] = bitget(rx_mux3U16,7)[0]
     

        #print(errFlag)


        return(errFlag)



## BATTERY
    def Battery():
        #bat = np.zeros(4)
        size_t = 2
        count=1
        for i in range(4):
            beginIndex = i*size_t
            endIndex= beginIndex+size_t
            tempData = np.ndarray((1,), buffer = payload[beginIndex:endIndex], dtype=np.uint16)
            if tempData.size == 1:
                bat[count] = tempData[0]
            count = count+2
            #print(bat)
        return(bat)


## XSENS
    def XSENS():
        xsens[1] = payload[60] #h
        xsens[3] = payload[61] #min
        xsens[5] = payload[64] #s
        xsens[7] = np.ndarray((1,), buffer = payload[62:64], dtype = np.uint16)[0] #ms
        xsens[9:14:2] = np.ndarray((3,), buffer = payload[0:12], dtype=np.dtype('>f4')) #Euler
        xsens[15:20:2] = np.ndarray((3,), buffer = payload[12:24], dtype=np.dtype('>f4')) #Pos
        xsens[21:26:2] = np.ndarray((3,), buffer = payload[24:36], dtype=np.dtype('>f4')) #AngV
        xsens[27:32:2] = np.ndarray((3,), buffer = payload[36:48], dtype=np.dtype('>f4')) #Acc
        xsens[33:38:2] = np.ndarray((3,), buffer = payload[48:60], dtype=np.dtype('>f4')) #V
        xsens[37] = np.double(xsens[5]) + np.double(xsens[7]/1000) #x_sec
        xsens[39] = 0
        #print(payload)
        #print(xsens[29:34:2])
        return(xsens)


## ADS
    def ADS():
        ads[1] = np.ndarray((1,), buffer = payload[0:4], dtype=np.dtype('>f4'))[0] #alt
        ads[3] = np.ndarray((1,), buffer = payload[4:8], dtype=np.dtype('>f4'))[0] #AoA
        ads[5] = np.ndarray((1,), buffer = payload[8:12], dtype=np.dtype('>f4'))[0] #sideslip
        ads[7] = np.ndarray((1,), buffer = payload[12:16], dtype=np.dtype('>u4'))[0] #v
        return(ads) 
    

## PPM
    def PPM():
        data = np.ndarray((16,), buffer = payload, dtype=np.dtype('>u2')) #v
        count = 1
        for i in range(int(len(ppm)/2)-1):
            #print(i)
            ppm[count] = data[i]
            count = count + 2
        #print(ppm)
        
        return(ppm) 
## DD
    def DD():
        return(dd)     

## ECU
    def ECU():
        #print(payload)
        ecuStr = (payload[2:-2]).tostring().decode("ascii")#payload[2:].astype('b') #evtl auch nutzbar in message_parser
        ecuStrList = list(ecuStr)
        # print(ecuStr)
        # print "".join([chr(item) for item in (payload[2:-2])])
        ecuFuel = payload[0] * 16 + payload[1]

        count = 1
        for i in range(int(len(ecuStrList)/2)):
            firstByte = ecuStrList[count-1]
            ecuStrList[count-1] = (ecuStrList[count])
            ecuStrList[count] = str(firstByte)
            count = count + 2

        #print(ecuStrList)
        ecuStrRearranged = "".join([str(elem) for elem in ecuStrList])
        strArray = ecuStrRearranged.replace('\x00','').replace('\r','').split(',')
        #print(ecuStrRearranged)
        #print(strArray)
        dataCount = len(strArray)

        if dataCount < 2:
            return(ecu)
        
        if strArray[1]=='WRP':
            ecu[7] = strArray[2]#.encode('ascii', 'ignore').decode('unicode_escape') #RPM control
        elif dataCount == 5:
            ecu[5] = strArray[0] #RPM actual
            ecu[11] = strArray[1]
            ecu[3] = strArray[2]
            ecu[9] = strArray[3]
            ecu[13] = strArray[4]

        if ecu[5] > 0:
            ecu[1] = 0.1911 * ecuFuel +0.0606
        
        #print(ecu)
        
        return(ecu)

        
## SERVO_REF
    def SERVO_REF():
        #print(PWM_coeff)
        data = np.ndarray((21,), buffer = payload, dtype=np.dtype('>u2'))
        count = 1
        for i in range(int(len(servo_ref)/2)-1):
            servo_ref[count] = data[i]*PWM_coeff[i][1]*0.2+PWM_coeff[i][2] #0.2 is for transformation to pulse microseconds
            count = count + 2
            #print(servo_ref[count-1])
            #print(PWM_coeff[i])
        #print(servo_ref)
        return(servo_ref) 


## IMU
    def IMU():
        
        #print(payload)
        varCount = IMU_noVar*IMU_noIMU
        u16_IMU = np.ndarray((varCount,), buffer = payload, dtype=np.dtype('>i2'))
        offsU16 = 0
        offsIMU = 0
        
        if IMU_1[0] == '1':
            imu[1:IMU_noIMU*2:2] = u16_IMU[offsU16:IMU_noIMU*IMU_noVar:IMU_noVar]
            offsU16 = offsU16 +1
            offsIMU = offsIMU + IMU_noIMU

        if IMU_1[1] == '1':
            imu[1:IMU_noIMU*2:2] = u16_IMU[offsU16:IMU_noIMU*IMU_noVar:IMU_noVar]
            offsU16 = offsU16 +1
            offsIMU = offsIMU + IMU_noIMU

        if IMU_1[2] == '1':
            imu[1:IMU_noIMU*2:2] = u16_IMU[offsU16:IMU_noIMU*IMU_noVar:IMU_noVar]
            offsU16 = offsU16 +1
            offsIMU = offsIMU + IMU_noIMU

        if IMU_1[3] == '1':
            imu[1:IMU_noIMU*2:2] = u16_IMU[offsU16:IMU_noIMU*IMU_noVar:IMU_noVar]
            offsU16 = offsU16 +1
            
        #print(imu)

        return(imu) 


## SHM
    def SHM():
        #print(SHM_coeff)
        varCount = SHM_noVar*SHM_noSHM
        u16_SHM = np.ndarray((varCount,), buffer = payload, dtype=np.dtype('>i2'))
        offsU16 = 0
        offsSHM = 0
       
        if SHM_1[0] == '1' and SHM_1[0] == '1':
           shm[1:SHM_noSHM*2:2] = (u16_SHM[0:SHM_noSHM*2-1:2])
           shm[SHM_noSHM*2+1:SHM_noSHM*4:2] = (u16_SHM[1:SHM_noSHM*2:2]*0.8057-500)/10
        count = 1
        for i in range(14):
            shm[count] = shm[count]*SHM_coeff[i][1]+SHM_coeff[i][2]
            count = count +2

        # if SHM_1[0] == '1':
        #     shm[1:SHM_noSHM*2:2] = u16_SHM[offsU16:SHM_noSHM*SHM_noVar:SHM_noVar]
        #     offsU16 = offsU16 +1
        #     offsSHM = offsSHM + SHM_noSHM

        # if SHM_1[1] == '1':
        #     shm[1:SHM_noSHM*2:2] = u16_SHM[offsU16:SHM_noSHM*SHM_noVar:SHM_noVar]
        #     offsU16 = offsU16 +1

        print(shm)            

        return(shm) 

    # map the inputs to the function blocks
    options = {0 : errorFlag,
            7 : Battery,
            14: XSENS,
            21: ADS, 
            28: PPM,
            35: DD,
            42: ECU,
            49: SERVO_REF,
            56: IMU,
            63: SHM
    }
    
    return(options[MsgID]())
                        