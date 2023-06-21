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

print(datetime.now())
# =============================================================================
# Create a Socket ( connect two computers)
# =============================================================================
try:
    host = "127.0.0.1"
    # host= socket.gethostname()
    print(host)
    port = 9997
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
# =============================================================================
# Listeining
# =============================================================================
def listener(client, address):

    print ("Accepted connection from: ", address)
    with clients_lock:
        clients.add(client)
    try:
        def commmunication():
            data = client.recv(1024)
            crc = Crc16.calc(data)
            # print(data, crc)
            global SATELLITE
####################### CHECK CRC ################
            if crc== 0:
# =============================================================================
# CHECK GET COMMAND
# =============================================================================
                print("Data", data)
                print(data[0])
                if data[0]==161:
                    
############################ CHECK GET SHIP DATA ##################
                    if data[1]==1:                               ####and data==b'\xa1\x01>n':
                        res = random.sample(range(100,10000), 40)
                        # print(res)
                        date_time=str(datetime.now())
                        print(date_time.encode())
                        xs = bytearray(b'')
                        for i in res:
                            s=i.to_bytes(2, 'big')
                            # print(s)
                            xs += s   
                        # print(xs+date_time.encode())
                        update_data= xs+date_time.encode()
                        crc=Crc16.calc(update_data)
                        update_data+= crc.to_bytes(2, 'big')
                        # print(crc, update_data, len(update_data))
                        client.send(update_data)
                        t2= time.time()

############################ CHECK GET sat info ##################
                    elif data[1]==2:
                        global flag
                        print(flag)
                        if flag==0:
                            msg=  bytes('gsat-7', 'utf-8')
                            crc = Crc16.calc(msg)
                            msg+= crc.to_bytes(2, 'big')### b'\xa1\x01>n'
                            # print(msg, len(crc.to_bytes(2, 'big')))
                            client.send(msg)
                        else:
                            print(SATELLITE)
                            client.send(SATELLITE)
                            print('+++++++++++++++++++++++++++++++')
                        print('3')
                    else:
                        print('no data to send')
# =============================================================================
# CHECK SET COMMAND
# =============================================================================
                elif data[0]==177:
############################ lock SATELLITE LOCK ##################
                    if data[1]==1:
                        flag=1
                        SATELLITE= data[4:]
                        print(SATELLITE)
                        sat_msg= ['satellite Locked']
                        msg=  bytes(sat_msg[0], 'utf-8')
                        crc = Crc16.calc(msg)
                        msg+= crc.to_bytes(2, 'big')### b'\xa1\x01>n'
                        # print(msg, len(crc.to_bytes(2, 'big')))
                        client.send(msg)
                        print('4')

############################ set home position ##################
                    elif data[1]==2:
                        print(data)
                        if data:
                            msg= "home position set"
                            client.send(msg.encode())
                            print('5')
############################ restart slsc ##################
                    elif data[1]==3:
                        if data:
                            msg= "slsc restart"
                            print(msg)
                            client.send(msg.encode())
                            print('6')
############################ shutdown slsc ##################
                    elif data[1]==4:
                        if data:
                            msg= "shutdown slsc"
                            print(msg)
                            client.send(msg.encode())
                            print('7')
############################ safemode ##################
                    elif data[1]==5:
                        if data:
                            msg= "safe mode"
                            print(msg)
                            client.send(msg.encode())
                            print('8')

                else:
                    print("data not found")
                    exit()
        print("begin timer")
        count = 1
        measure1 = time.time()
        print(measure1)
        measure2 = time.time()
        print(measure2)
        print('measured time:',measure2 - measure1 )
        while count==1 :
            if measure2 - measure1 >= 0:
                # print("two seconds")
                measure1 = measure2
                measure2 = time.time()
                commmunication()
            else:
                measure2 = time.time()
    finally:
        with clients_lock:
            clients.remove(client)
            print("exit")
            client.close()
clients = set()
clients_lock = threading.Lock()

while True:
    client, address = s.accept()
    print("connected")
    client.settimeout(10.0)
    print(client, address)
    th.append(Thread(target=listener, args = (client,address)).start())
    # s.settimeout(3)
s.close()

