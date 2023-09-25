# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 13:31:55 2023

@author: RND5
"""
" Imported Libraries "
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 13:31:55 2023

@author: RND5
"""
" Imported Libraries "
from ftplib import FTP
import time
import socket
import os
from threading import Thread
import threading
import time
import datetime
import random
from datetime import datetime, date
import struct
from datetime import datetime
import csv
import io


def dataLog_setup():
    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")
    folder_name = str(current_year) + "-" + str(current_month)
    # Check if the folder exists using os.path.exists()
    if os.path.exists(folder_name):
        print("The folder exists.")
    else:
        print("The folder does not exist.")
        os.makedirs(folder_name)
    return folder_name


csv_filename = os.path.join(dataLog_setup(), "LOG-{}.csv".format(datetime.now().date()))


def write_to_slscStatusLog(status):
    # Create the CSV file with today's date
    with open(csv_filename, "a", newline="") as file:
        # using csv.writer method from CSV package
        write = csv.writer(file)
        write.writerow(status)
        file.close()


def write_to_tempCsv(filename, data):
    # Check if lock file exists
    lock_file = filename + ".lock"
    if os.path.exists(lock_file):
        print("File is already in use.")
        return
    try:
        # Create lock file
        open(lock_file, "w").close()
        # Open the CSV file and write data
        with open(filename, "w", newline="") as csvfile:
            # Write data to CSV file
            # ...
            write = csv.writer(csvfile)
            write.writerow(data)
            csvfile.close()

        print("File write completed successfully.")

    finally:
        # Remove lock file
        print("delete")
        if os.path.exists(lock_file):
            os.remove(lock_file)


" Imported Software Module related files "
# import EthernetComm_V1_0
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
SatelliteName = "Vikram Lander"

SYSHealthFlag = 0  # done
OSUFlag = 0  # done
GPSFlag = 0  # done
OFCFlag = 0  # done
BeaconFlag = 0  # done
SatelliteLockFlag = 0  # done
GPSLockFlag = 0  # done
azEnFlag = 0
elEnFlag = 0
crElEnFlag = 0
polEnFlag = 0

SystemTemp = 0
OSURoll = 0
OSUPitch = 0
OSUYaw = 0
BeaconPower = 0
BeaconFreq = 0
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

MotorElCurrent = 0  # done
MotorxELCurrent = 0  # done
MotorAzCurrent = 0  # done
MotorPolCurrent = 0  # done

BUCCurrent = 0
OpticalFibreCurrent = 0
SLSCCurrent = 0
TotalSysCurrent = 0


def list_of_param():
    csvPara = [
        SatelliteName,
        OSUFlag,
        GPSFlag,
        BeaconFlag,
        OFCFlag,
        azEnFlag,
        elEnFlag,
        crElEnFlag,
        polEnFlag,
        GPSLockFlag,
        SatelliteLockFlag,
        SYSHealthFlag,
        TimeStamp,
        SystemTemp,
        OSURoll,
        OSUPitch,
        OSUYaw,
        BeaconPower,
        BeaconFreq,
        GPSTime, #19
        GPSLat,
        GPSLong,
        TargetAz,
        TargetEl,
        TargetPolSkew,
        CurrentPosEl,
        CurrentPosxEl,
        CurrentPosAzimuth,
        CurrentPosPol,
        MotorElCurrent,
        MotorxELCurrent,
        MotorAzCurrent,
        MotorPolCurrent,
        BUCCurrent,
        OpticalFibreCurrent,
        SLSCCurrent,
        TotalSysCurrent,
    ]
    return csvPara


# Wait for 2 seconds to give time to hardware to boot properly
time.sleep(2)

# 4- OSU is powered up, COMM is checked and Flag is set. (if no COMM , Error=Faulty Unit)
time.sleep(0.1)
OSUFlag = 1
print("osu flag set: ", list_of_param())
write_to_slscStatusLog(list_of_param())
write_to_tempCsv("temp_data.csv", list_of_param())

# 5- GPS is powered up, COMM is checked and Flag is set. (if no COMM , Error=Faulty Unit)
time.sleep(0.1)
GPSFlag = 1
print("gps flag set: ", list_of_param())
write_to_slscStatusLog(list_of_param())
write_to_tempCsv("temp_data.csv", list_of_param())

# 6- Beacon Tracker is powered up, COMM is checked and Flag is set. (if no COMM , Error=Faulty Unit)
time.sleep(0.1)
BeaconFlag = 1
print(" beacon flag set: ", list_of_param())
write_to_slscStatusLog(list_of_param())
write_to_tempCsv("temp_data.csv", list_of_param())

# 7- RFoverFibre Transmitter and Receiver is powered up, Current consumption is checked and Flag is set. (if current outside limits , Error=Faulty Unit)
time.sleep(0.1)
OFCFlag = 1
print("ofc flag set: ", list_of_param())
write_to_slscStatusLog(list_of_param())
write_to_tempCsv("temp_data.csv", list_of_param())


# 9- Power to Motor Control Cards 1-4 is given by relay card. Encoder positions 1-4 are read.
# This is used to get position of axes and decide if they are at parking or home position or somewhere else

# 10- Give power to Motors using relay card

# 11- Release breaks of all four motors

# 12- Monitor nominal motor current (i.e. current at holding torque) and Flag is set. (if current outside limits , Error=Faulty Unit) else Motor Initiation completed.
MotorElCurrent = 0
MotorxELCurrent = 0
MotorAzCurrent = 0
MotorPolCurrent = 0
print(list_of_param())
write_to_slscStatusLog(list_of_param())
write_to_tempCsv("temp_data.csv", list_of_param())

# encoder flag set
time.sleep(0.1)
azEnFlag = 1
elEnFlag = 1
crElEnFlag = 1
polEnFlag = 1
print("encoder flag set: ", list_of_param())
write_to_slscStatusLog(list_of_param())
write_to_tempCsv("temp_data.csv", list_of_param())
# 13- Wait for user command CASE A: Go to Default Satellite , CASE B: Load Satellite

# 14- Wait for GPS to achieve satellite lock , get lat, long and time. Set Flag GPS LOCK (if no lock in 15mins , ERR=Check GPS unit, GPS antenna cable etc)
time.sleep(5)
GPSLockFlag = 1
print("gps lock flag set: ", list_of_param())
write_to_slscStatusLog(list_of_param())
write_to_tempCsv("temp_data.csv", list_of_param())

# 15- Move motors to nominal position of satellite using SLSC algo with inputs of GPS, OSU and Encoders
time.sleep(5)
SatelliteLockFlag = 1
print("sat lock flag set: ", list_of_param())
write_to_slscStatusLog(list_of_param())
write_to_tempCsv("temp_data.csv", list_of_param())


SYSHealthFlag = 1
print("sys health flag set: ", list_of_param())
write_to_slscStatusLog(list_of_param())
write_to_tempCsv("temp_data.csv", list_of_param())

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
    OSURoll = round(random.uniform(-30.0, 30.0), 1)
    OSUPitch = round(random.uniform(-15.0, 15.0), 1)
    OSUYaw = round(random.uniform(0.0, 359.9), 1)
    BeaconPower = round(random.randint(-80, -60), 1)
    BeaconFreq = 11698.50
    TimeStamp = round(time.time(), 3)
    GPSTime = round(time.time(), 3)  # now.strftime("%H:%M:%S")
    GPSLat = 19.0760
    GPSLong = 72.8777

    TargetAz = round(random.uniform(-30.0, 30.0), 1)
    TargetEl = round(random.uniform(-15.0, 15.0), 1)
    TargetPolSkew = round(random.uniform(-5.0, 5.0), 1)

    CurrentPosEl = round(TargetEl + round(random.uniform(0, 0.5), 1), 1)
    CurrentPosxEl = round(TargetEl + round(random.uniform(0, 0.5), 1), 1)
    CurrentPosAzimuth = round(TargetAz + round(random.uniform(0, 0.5), 1), 1)
    CurrentPosPol = round(TargetPolSkew + round(random.uniform(0, 0.5), 1), 1)

    MotorElCurrent = round(random.uniform(0.5, 2.0), 1)  # done
    MotorxELCurrent = round(random.uniform(0.5, 2.0), 1)  # done
    MotorAzCurrent = round(random.uniform(0.5, 2.0), 1)  # done
    MotorPolCurrent = round(random.uniform(0.5, 2.0), 1)  # done

    SystemTemp = round(random.randint(-10, 60), 1)

    BUCCurrent = round(random.uniform(0.5, 2), 1)
    OpticalFibreCurrent = round(random.uniform(0.5, 2), 1)
    SLSCCurrent = round(random.uniform(0.5, 2), 1)
    TotalSysCurrent = round(
        SLSCCurrent
        + MotorElCurrent
        + MotorxELCurrent
        + MotorAzCurrent
        + MotorPolCurrent
        + BUCCurrent
        + OpticalFibreCurrent,
        1,
    )

    # print(list_of_param())
    t1 = time.time()
    write_to_slscStatusLog(list_of_param())
    write_to_tempCsv("temp_data.csv", list_of_param())
    # print(time.time()-t1)
    time.sleep(0.01)
