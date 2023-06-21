import socket
import sys
from threading import Thread
import socket
import time
from crccheck.crc import Crc16

s = socket.socket()  
host = "192.168.13.18"
print(host)      
port = 9999

s.connect((host, port))
print('connected')
class command:
    # =============================================================================
    # GET SHIP DATA
    # =============================================================================
    def shipData(self):
        msg = bytearray([161,1]) ###b'\xa1\x01'
        crc = Crc16.calc(msg)
        msg+= crc.to_bytes(2, 'big')### b'\xa1\x01>n'
        return msg
    # =============================================================================
    # GET SLSC HEALTH STATUS
    # =============================================================================
    def getLockedSat(self):
        msg = bytearray([161,2]) ###b'\xa1\x02'
        crc = Crc16.calc(msg)
        msg+= crc.to_bytes(2, 'big')### b'\xa1\x02\x0e\r'
        return msg
  
    # =============================================================================
    # LOCK SATELLITE
    # =============================================================================
    def lockSatellite(self):
        msg = bytearray([177,1])  ### bytearray(b'\xb1\x01'
        crc = Crc16.calc(msg) ### 15645 
        msg+= crc.to_bytes(2, 'big')### b'=\x1d'
        # print(msg) #### bytearray(b'\xb1\x01=\x1d')
        return msg
    # =============================================================================
    # BOOT SYSTEM
    # =============================================================================
    def homePosition(self): 
        msg = bytearray([177,2])  ### bytearray(b'\xb1\x02')
        crc = Crc16.calc(msg) ### 3454
        msg+= crc.to_bytes(2, 'big')### b'\r~' 
        print(msg) #### bytearray(b'\xb1\x02\r~')
        return msg
    # =============================================================================
    # READ POSITION MOTOR
    # =============================================================================
    def restartSLSC(self):
        msg = bytearray([177,3]) ### bytearray(b'\xb1\x03')
        crc = Crc16.calc(msg) ### 7519 
        msg+= crc.to_bytes(2, 'big')### b'\x1d_'
        # print(msg) #### bytearray(b'\xb1\x03\x1d_')
        return msg
    # =============================================================================
    # BOOT osu
    # =============================================================================
    def shutdownSLSC(self):
        msg = bytearray([177,4]) ### b'\xb1\x04'
        crc = Crc16.calc(msg) ### 28088
        msg+= crc.to_bytes(2, 'big')### b'\r~' 
        # print(msg) #### bytearray(b'\xb1\x04m\xb8')
        return msg
        # =============================================================================
    # BOOT mu
    # =============================================================================
    def safemodeSLSC(self):
        msg = bytearray([177,5])  ### bytearray(b'\xb1\x05')
        crc = Crc16.calc(msg) ### 32153
        msg+= crc.to_bytes(2, 'big')#### bytearray(b'\xb1\x05}\x99')
        return msg

# =============================================================================
# GET ALL DATA TO UPDATAE DATA TO GUI
# =============================================================================
def getUpdateData():
    value= s.sendall(command().shipData())
    global byte_data
    byte_data = s.recv(100000)
    date_time= byte_data[80:106] ###### current date and time from slsc
    crc=  Crc16.calc(byte_data)
    print(crc, byte_data)
    if len(byte_data)==108:
        if crc==0:
            c=0
            shifted= []
            for i in range(len(byte_data)):
                if c<= 80:
                    shifted_byte1 =  ((byte_data[c]<<8)&0xff00) | ((byte_data[c+1])&0xff)
                    # print(c, shifted_byte1)
                    shifted.append(shifted_byte1)
                    c += 2
                    # print('incremented bytes: ', c)
                else:
                    # print('stop')
                    break
            global data_float
            data_float= []
            for val in shifted:
                data_float.append(val/100)
    else:
        print('data not found')
# =============================================================================
# set lock satellite command
# =============================================================================
def getLockSatellite():
    print('dfvsdfv')
    value2= s.sendall(command().getLockedSat())
    get_sat = s.recv(100000)
    global satellite_name
    satellite_name= get_sat[:-2].decode()
    print(get_sat, satellite_name)
    crc = Crc16.calc(get_sat)
    print(crc)
# =============================================================================
# set lock satellite command
# =============================================================================
def setLockSatellite(LOCK): # LOCK = user select satellite from table 
    cmd= command().lockSatellite()+LOCK
    # print(cmd)
    crc = Crc16.calc(cmd) ### 24027
    cmd+= crc.to_bytes(2, 'big')
    value2= s.sendall(cmd)
    lock_recv= s.recv(100000)
    # print(lock_recv)
    lock_crc= Crc16.calc(lock_recv)
    print('locked satellite', lock_crc)
    if lock_crc==0:
        print('locked')
    else:
        print('mo satellite locked')
# =============================================================================
# SET HOME POSITION
# =============================================================================
def setHomePosition():
    value= s.sendall(command().homePosition())
    byte_home_position = s.recv(1000)

    if byte_home_position:
        print(byte_home_position.decode())
    else:
        print("len of bytes not correct")
# =============================================================================
# send boot cmd
# =============================================================================
def setRestart():
    value3= s.sendall(command().restartSLSC())
    rec_data = s.recv(100000)
    print(rec_data.decode())
# =============================================================================
# send boot cmd
# =============================================================================
def setShutdown():
    value3= s.sendall(command().shutdownSLSC())
    rec_data = s.recv(100000)
    print(rec_data.decode())
# =============================================================================
# send boot cmd
# =============================================================================
def setSafemode():
    value3= s.sendall(command().safemodeSLSC())
    rec_data = s.recv(100000)
    print(rec_data.decode())
getUpdateData()