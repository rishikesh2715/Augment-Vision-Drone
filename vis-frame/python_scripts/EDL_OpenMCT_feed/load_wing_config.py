import pandas as pd
import math
import numpy as np




wingConfig = pd.read_excel('Wing_0.xlsx', header = [1,2,4],dtype={'Name': str, 'Value': float})
wingConfigList = wingConfig.values.tolist()

section_names = ['Left wing', 'Right wing', 'Left tail', 'Right tail', 'Airbrakes']


#print(wingConfig['Left wing']['Flap L3'])#.get('Left wing'))
def getCoefficients(who):

    def xlsReader(wingConfig):
        flap = [[],[],[],[],[],[],[]] #shm; shmDeg; SHMID; pwm; pmwDEG; pwm ID; correction
        
        count = 0
        for part in wingConfig['SHM'][:]:
            #print(part)
            #print(type(part))
            if ((type(part) == int or type(part) == float) and (count<12 and not(math.isnan(part)))):
                flap[0].append(part) #SHM
                #print(count)
            if ((type(part) == int or type(part) == float) and (12<=count<21 and not(math.isnan(part)))):
                flap[3].append(part) #PWM
            if (count == 24):
                flap[2] = part #shm ID
            if (count == 30):
                flap[6] = part #correction
            count = count +1

        count = 0
        for part in wingConfig['DEG'][:]:
            #print(part)
            #print(type(part))
            if ((type(part) == int or type(part) == float) and (count<12 and not(math.isnan(part)))):
                flap[1].append(part) #shm DEG
                #print(count)
            if ((type(part) == int or type(part) == float) and (12<=count<21 and not(math.isnan(part)))):
                flap[4].append(part) #pwm DEG
            if (count == 24):
                flap[5] = part #pwm ID
        
            count = count +1

        coefficientsSHM = np.polyfit(flap[0],flap[1],1)
        coefficientsPWM = np.polyfit(flap[3],flap[4],1)
        #print(flap)
        return((flap[2], coefficientsSHM[0],coefficientsSHM[1], flap[6]), (flap[5], coefficientsPWM[0],coefficientsPWM[1], flap[6]))

    SHM=[]
    PWM=[]
    count=1
    for num in range(4):
        #print('Flap L'+str(4-count))
        LeftWing = xlsReader(wingConfig['Left wing']['Flap L'+str(5-count)])
        SHM.append(LeftWing[0])
        PWM.append(LeftWing[1])
        RightWing = xlsReader(wingConfig['Right wing']['Flap R'+str(count)])
        SHM.append(RightWing[0])
        PWM.append(RightWing[1])
        count=count+1

    count=1
    for num in range(2):
        #print('Tail L'+str(3-count))
        LeftTail = xlsReader(wingConfig['Left tail']['Tail L'+str(3-count)])
        SHM.append(LeftTail[0])
        PWM.append(LeftTail[1])
        RightTail = xlsReader(wingConfig['Right tail']['Tail R'+str(count)])
        SHM.append(RightTail[0])
        PWM.append(RightTail[1])
        count=count+1

    Airbrakes = xlsReader(wingConfig['Airbrakes']['Airbrake L'])
    SHM.append(Airbrakes[0])
    PWM.append(Airbrakes[1])
    Airbrakes = xlsReader(wingConfig['Airbrakes']['Airbrake R'])
    SHM.append(Airbrakes[0])
    PWM.append(Airbrakes[1])

    # fill in the empty channels for more easy parsing
    PWM.append((5,0,0))
    PWM.append((6,0,0))
    PWM.append((13,0,0))
    PWM.append((14,0,0))
    PWM.append((19,0,0))
    PWM.append((20,0,0))


    #print(xlsReader(wingConfig['Left tail']['Tail L2'][:]))
    if who=='PWM':
        return(sorted(PWM))
    if who=='SHM':
        return(sorted(SHM))
    # print(sorted(PWM))
    # print(sorted(SHM))


