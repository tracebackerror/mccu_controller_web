# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 13:31:55 2023

@author: RND5
"""
" Imported Libraries "

import socket
import os
from threading import Thread
import threading
import time
import datetime
import random
from crccheck.crc import Crc16, CrcXmodem
from datetime import datetime, date
import struct
from datetime import datetime
import csv

" Imported Software Module related files "
#import EthernetComm_V1_0
# import IMU_V1_0
# import MotorControl_V1_0
# import OSU_V1_0
# import StabAlgo_V1_0
# import StepTrack_V1_0

# Above Deck Equipment (ADE) boot sequence
# 1- when POWER ON, AC power goes to +48V and +24C DC supplies

# 2- Power goes to Ethernet Media Converter by default since it connects ADE and BDE over fibre

# 3- Beagle bone boots, all other systems are cutoff from power with help of solid state relays

# Initialise variables, arrays
TimeStamp = 0
SatelliteName = "GSAT-10"

SYSHealthFlag = 0 #done
OSUFlag = 0 #done
GPSFlag = 0 #done
OFCFlag = 0 #done
BeaconFlag = 0 #done
SatelliteLockFlag = 0 #done
GPSLockFlag = 0 #done
TotalSysCurrent = 0 #done

SystemTemp = 0
OSURoll = 0
OSUPitch = 0
OSUYaw = 0
BeaconPower  = 0
BeaconFreq  = 0
GPSTime = 0
GPSLat = 0
GPSLong = 0
TargetAz = 0
TargetEl = 0
TargetPolSkew = 0
CurrentPosEl = 0
CurrentPosxEl = 0
CurrentPosAzimuth = 0
CurrentPosPol = 0

MotorElCurrent = 0 #done
MotorxELCurrent = 0 #done
MotorAzCurrent = 0 #done
MotorPolCurrent = 0 #done

BUCCurrent = 0
OpticalFibreCurrent = 0
SLSCCurrent = 0

# Wait for 2 seconds to give time to hardware to boot properly
time.sleep(2)

# 4- OSU is powered up, COMM is checked and Flag is set. (if no COMM , Error=Faulty Unit)
time.sleep(0.1)
OSUFlag = 1
csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
           TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
           GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
           CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
           BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
print(csvPara)

with open('data_str.csv', 'a', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
with open('temp_data_str.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
    
    
    
# 5- GPS is powered up, COMM is checked and Flag is set. (if no COMM , Error=Faulty Unit)
time.sleep(0.1)
GPSFlag = 1
csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
           TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
           GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
           CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
           BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
print(csvPara)

with open('data_str.csv', 'a', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
with open('temp_data_str.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
    
    
# 6- Beacon Tracker is powered up, COMM is checked and Flag is set. (if no COMM , Error=Faulty Unit)
time.sleep(0.1)
BeaconFlag = 1

csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
           TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
           GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
           CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
           BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
print(csvPara)

with open('data_str.csv', 'a', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
with open('temp_data_str.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
    
# 7- RFoverFibre Transmitter and Receiver is powered up, Current consumption is checked and Flag is set. (if current outside limits , Error=Faulty Unit)
time.sleep(0.1)
OFCFlag = 1

csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
           TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
           GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
           CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
           BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
print(csvPara)

with open('data_str.csv', 'a', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
with open('temp_data_str.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
    
    
# 8- Overall total current of +24V DC supply is checked and Flag is set. (if current outside limits , Error=Faulty Unit) else BOOT completed.
time.sleep(0.1)
TotalSysCurrent = 1

csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
           TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
           GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
           CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
           BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
print(csvPara)

with open('data_str.csv', 'a', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
with open('temp_data_str.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
    
    
# 9- Power to Motor Control Cards 1-4 is given by relay card. Encoder positions 1-4 are read.
# This is used to get position of axes and decide if they are at parking or home position or somewhere else

# 10- Give power to Motors using relay card

# 11- Release breaks of all four motors

# 12- Monitor nominal motor current (i.e. current at holding torque) and Flag is set. (if current outside limits , Error=Faulty Unit) else Motor Initiation completed.
MotorElCurrent = 0
MotorxELCurrent = 0
MotorAzCurrent = 0
MotorPolCurrent = 0

csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
           TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
           GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
           CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
           BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
print(csvPara)

with open('data_str.csv', 'a', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
with open('temp_data_str.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
    
    
# 13- Wait for user command CASE A: Go to Default Satellite , CASE B: Load Satellite

# 14- Wait for GPS to achieve satellite lock , get lat, long and time. Set Flag GPS LOCK (if no lock in 15mins , ERR=Check GPS unit, GPS antenna cable etc)
time.sleep(5)
GPSLockFlag = 1

csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
           TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
           GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
           CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
           BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
print(csvPara)

with open('data_str.csv', 'a', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
with open('temp_data_str.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
    
    
# 15- Move motors to nominal position of satellite using SLSC algo with inputs of GPS, OSU and Encoders
time.sleep(5)
SatelliteLockFlag = 1

csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
           TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
           GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
           CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
           BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
print(csvPara)

with open('data_str.csv', 'a', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
with open('temp_data_str.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
    


SYSHealthFlag = 1

csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
           TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
           GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
           CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
           BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
print(csvPara)

with open('data_str.csv', 'a', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
with open('temp_data_str.csv', 'w', newline='') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(csvPara)
    f.close()
    
# 16- Power on the LNBC

# 17- Boot Completed and ready for tracking

# 18- Continuous tracking process is initiated



# demoan stops.

# ________________________________________________________________________________________________________________________________________________
# RUN TIME TRACKING ROUTINE
# 1- SET Satellite (Default or user) read from CSV file dump at boot sequence
# 2- SET beacon tracker with correct LO freq
now = datetime.now()
while True:
    
    # 3- Use SLSC Algo to get required motor positions EL, XEL, ROLL, YAWSystemTemp = 0
    OSURoll = round(random.uniform(-30.0,30.0),1)
    OSUPitch = round(random.uniform(-15.0,15.0),1)
    OSUYaw = round(random.uniform(0.0,359.9),1)
    BeaconPower  = round(random.randint(-80,-60),1)
    BeaconFreq  = 11698.50
    TimeStamp = round(time.time(),3)
    GPSTime = round(time.time(),3) #now.strftime("%H:%M:%S")
    GPSLat = 19.0760
    GPSLong = 72.8777
    
    TargetAz = round(random.uniform(-30.0,30.0),1)
    TargetEl = round(random.uniform(-15.0,15.0),1)
    TargetPolSkew = round(random.uniform(-5.0,5.0),1)
    
    CurrentPosEl = round(TargetEl + round(random.uniform(0,0.5),1),1)
    CurrentPosxEl = round(TargetEl + round(random.uniform(0,0.5),1),1)
    CurrentPosAzimuth = round(TargetAz + round(random.uniform(0,0.5),1),1)
    CurrentPosPol = round(TargetPolSkew + round(random.uniform(0,0.5),1),1)
    
    MotorElCurrent = round(random.uniform(0.5, 2.0),1) #done
    MotorxELCurrent = round(random.uniform(0.5, 2.0),1) #done
    MotorAzCurrent = round(random.uniform(0.5, 2.0),1) #done
    MotorPolCurrent = round(random.uniform(0.5, 2.0),1) #done
    
    SystemTemp = round(random.randint(-10, 60),1)
    
    BUCCurrent = round(random.uniform(0.5, 2),1)
    OpticalFibreCurrent = round(random.uniform(0.5, 2),1)
    SLSCCurrent = round(random.uniform(0.5, 2),1)
    TotalSysCurrent = round(SLSCCurrent + MotorElCurrent + MotorxELCurrent + MotorAzCurrent + MotorPolCurrent + BUCCurrent + OpticalFibreCurrent,1)
    
    csvPara = [SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
               TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
               GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
               CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
               BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent]
    # print(csvPara)
    list_string = map(str, csvPara)
    with open('data_str.csv', 'a', newline='') as f:
        # COLUMNS :- SatelliteName, SYSHealthFlag, OSUFlag, GPSFlag, OFCFlag, BeaconFlag, SatelliteLockFlag, GPSLockFlag, 
        #    TimeStamp, SystemTemp, OSURoll, OSUPitch, OSUYaw, BeaconPower,BeaconFreq, 
        #    GPSTime, GPSLat, GPSLong, TargetAz, TargetEl, TargetPolSkew, CurrentPosEl, CurrentPosxEl, 
        #    CurrentPosAzimuth, CurrentPosPol, MotorElCurrent, MotorxELCurrent, MotorAzCurrent, MotorPolCurrent,
        #    BUCCurrent, OpticalFibreCurrent, SLSCCurrent, TotalSysCurrent
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(csvPara)
        f.close()
    with open('temp_data_str.csv', 'w', newline='') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(csvPara)
        f.close()
    time.sleep(0.1)
    # 4- Move motors as per calculated positions
    # 5- use STEP TRACK Algo and refine positions
    # 6- Write a complete dump of LOG in given format in CSV
    # 7- GOT to STEP 3



    


# STEP 3-STEP 7 iterative loop of 100mSec