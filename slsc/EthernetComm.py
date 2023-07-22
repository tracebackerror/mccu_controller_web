# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 13:02:41 2023

@author: RND2
"""

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
import errno
print(datetime.now())
# =============================================================================
# Create a Socket ( connect two computers)
# =============================================================================
try:
    host = "127.0.0.1"
    # host= socket.gethostname()
    print(host)
    port = 9999
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket formed ")
except socket.error as msg:
    print("Socket creation error: " + str(msg))
 
# =============================================================================
# Binding the socket and listening for connections
# =============================================================================
try:
    print("Binding the Port: " + str(port))
    s.bind((host,port))
    s.listen(3)
except socket.error as msg:
    print("Socket Binding error" + str(msg) + "\n" + "Retrying...")

th= [] 
global flag
flag=0
def is_file_in_use(filename):
    lock_file = filename + '.lock'
    return os.path.exists(lock_file)

def read_temp_file():
    with open('temp_data.csv', mode ='r')as file:
    # reading the CSV file
        first_item = file.readline().strip()
        csvFile = csv.reader(file)
        # file_size = os.path.getsize('temp_data_str.csv')
        # print(first_item)
        file.close()
    return first_item
# =============================================================================
# Listeining
# =============================================================================
filename = 'temp_data.csv'
buffer_time = 0.03  # Buffer time in seconds

def listener(client, address):
    # print ("Accepted connection from: ", address)
    # with clients_lock:
    #     clients.add(client)
    try:
        data = client.recv(1024)
        crc = Crc16.calc(data)
        # print(data[0], data[1], crc)
        global SATELLITE
####################### CHECK CRC ################
        if crc==0:
# =============================================================================
# CHECK GET COMMAND
# =============================================================================
            if data and data[0]==161:
############################ CHECK GET SHIP DATA ##################
                if data[1]==1: 
                    # print((1))                              ####and data==b'\xa1\x01>n':
                    t1= time.time()
                    if is_file_in_use(filename):
                        print("The file is currently in use.")
                        start_time = time.time()
                        while is_file_in_use(filename):
                            elapsed_time = time.time() - start_time
                            # print(start_time, time.time())
                            if elapsed_time >= buffer_time:
                                print("Timeout: The file is still in use.")
                                data_nac = bytes([1])
                                crc=Crc16.calc(data_nac)
                                data_nac+= crc.to_bytes(2, 'big')
                                print(data_nac)
                                client.send(data_nac)
                                print('nac')
                                break
                            else:
                                print("Waiting for the file to be freed...")
                        
                        if not is_file_in_use(filename):
                            print("The file is now freed. Perform further actions.")

                            data_encoded = bytes(read_temp_file(),'UTF-8')
                            crc=Crc16.calc(data_encoded)
                            data_encoded+= crc.to_bytes(2, 'big')
                            print(data_encoded)
                            client.send(data_encoded)
                    else:
                        print("The file is not in use.")
                    # print(read_temp_file())
                        data_encoded = bytes(read_temp_file(),'UTF-8')
                        crc=Crc16.calc(data_encoded)
                        data_encoded+= crc.to_bytes(2, 'big')
                        # print(data_encoded)
                        client.send(data_encoded)

                    t2= time.time()
                    print('time : ', t2-t1)

############################ CHECK GET sat info ##################
                elif data[1]==2:
                    global flag
                    print(flag)
                    if flag==0:
                        msg=  bytes(read_temp_file()[0], 'utf-8')
                        crc = Crc16.calc(msg)
                        msg+= crc.to_bytes(2, 'big')### b'\xa1\x01>n'
                        # print(msg, len(crc.to_bytes(2, 'big')))
                        sat_na=read_temp_file().split(',')[0]
                        print('s=', sat_na)
                        client.send(bytes(sat_na, 'utf-8'))
                    else:
                        print(SATELLITE)
                        locked_sat=SATELLITE.decode('utf-8').split(" ")[0]
                        # print(locked_sat, bytes(locked_sat, 'utf-8'))
                        # crc = Crc16.calc(SATELLITE)
                        # SATELLITE+= crc.to_bytes(2, 'big')### b'\xa1\x01>n'
                        client.send(bytes(locked_sat, 'utf-8'))
                        print('+++++++++++++++++++++++++++++++')
                    print('3')
                else:
                    print('no data to send')
# =============================================================================
# CHECK SET COMMAND
# =============================================================================
            elif data and data[0]==177:
############################ lock SATELLITE LOCK ##################
                if data[1]==1:
                    print(data)
                    flag=1
                    SATELLITE= data[2:-2]
                    print(SATELLITE)
            
                    msg=  bytes([1])
                    crc = Crc16.calc(msg)
                    msg+= crc.to_bytes(2, 'big')### b'\xa1\x01>n'
                    print(msg, len(crc.to_bytes(2, 'big')))
                    client.send(msg)
                    print('4')

############################ set home position ##################
                elif data[1]==2:
                    print(data)
                    if data:
                        msg= bytes([1])
                        crc = Crc16.calc(msg)
                        msg+= crc.to_bytes(2, 'big')
                        print(msg)
                        client.send(msg)
                        print('5')
############################ restart slsc ##################
                elif data[1]==3:
                    if data:
                        msg= bytes([1])
                        crc = Crc16.calc(msg)
                        msg+= crc.to_bytes(2, 'big')
                        print(msg)
                        client.send(msg)
                        print('6')
############################ shutdown slsc ##################
                elif data[1]==4:
                    if data:
                        msg= bytes([1])
                        crc = Crc16.calc(msg)
                        msg+= crc.to_bytes(2, 'big')
                        print(msg)
                        client.send(msg)
                        print('7')
############################ safemode ##################
                elif data[1]==5:
                    if data:
                        msg= bytes([1])
                        crc = Crc16.calc(msg)
                        msg+= crc.to_bytes(2, 'big')
                        print(msg)
                        client.send(msg)
                        print('8')

            else:
                print("data not found")
                exit()
        # print("begin timer")
        # count = 1
        # measure1 = time.time()
        # print(measure1)
        # measure2 = time.time()
        # print(measure2)
        # print('measured time:',measure2 - measure1 )
        # while count==1 :
        #     if measure2 - measure1 >= 0:
        #         # print("two seconds")
        #         measure1 = measure2
        #         measure2 = time.time()
        #         commmunication()
        #     else:
        #         measure2 = time.time()
    finally:
        # with clients_lock:
            # clients.remove(client)
        print("exit")
        client.close()
clients = set()
clients_lock = threading.Lock()

while True:
    client, address = s.accept()
    print("connected")
    client.settimeout(10.0)
    # print(client, address)

    listener(client, address)
    # th.append(Thread(target=listener, args = (client,address)).start())
    # s.settimeout(3)
s.close()

