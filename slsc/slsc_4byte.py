""" """ """ """ """ """ """ """ """ """ """ slsc """ """ """ """ """ """ """ """ """ """ """
import random
from crccheck.crc import Crc16, CrcXmodem
from datetime import datetime, date

from datetime import datetime
    ####and data==b'\xa1\x01>n':
# lat= 19.07 +'N'    
# long=72.87 +'E'     

lat= [int(19.0760*10000)]    
long=[int(72.8777*10000)]
roll = [int(round(random.uniform(-25.0000, 25.0000), 4)*10000) ] 
pitch = [int(round(random.uniform(-15.0000, 15.0000), 4)*10000) ]
yaw =  [int(round(random.uniform(-8.0000, 8.0000), 4)*10000) ]
temp = [int(round(random.uniform(5.0000, 25.0000), 4)*10000) ]
curr= [int(round(random.uniform(8.0000, 10.0000), 4)*10000) ]
# print(int(round(random.uniform(-25.00, 25.00), 2)*100), (int(round(random.uniform(-25.00, 25.00), 2)*100)).to_bytes(2, 'big', signed=True))
# print(int(lat), int(long), int(roll), int(pitch) , int(yaw), int(temp), int(curr))
lst= lat +long+roll+pitch+yaw+temp+curr   
print('orignal list', lst)

xs = bytearray(b'')
for i in lst:
    s=i.to_bytes(4, 'big', signed=True)
    xs += s 
    # print(s[1:2])  
print(xs, len(xs))




""" """ """ """ """ """ """ """ """ """ """ MCCU  """ """ """ """ """ """ """ """ """ """ """
''' received data xs in bytes conversion '''
byte_data= []
lsb=4
msb=0
for i in xs:
    if msb<= 27:
        byte= int.from_bytes(xs[msb:lsb], "big", signed=True)
        lsb += 4
        msb +=4
        byte_data.append(byte)
    else:
        break
print(byte_data )
update_data=[]
for i in byte_data:
    data= i/10000
    update_data.append(data)
print(update_data)
""" """ """ """ """ """ """ """ """ """ """ MCCU  """ """ """ """ """ """ """ """ """ """ """


# shifted= []
# c=0
# for i in range(len(xs)):
#     if c<= 27:
#         shifted_byte1 = ((xs[c]<<24)&0xff000000) | ((xs[c+1]<<16)&0xff0000) | ((xs[c+2]<<8)&0xff00) | ((xs[c+3])&0xff)
#         # if (shifted_byte1 & 0x80):
#         #     shifted_byte1 = shifted_byte1 - 1
#         #     shifted_byte1 = ~shifted_byte1
#         #     print(shifted_byte1)
#         shifted.append(shifted_byte1)
#         c += 4
#     else:
#         break
# print('shifted bytes lst: ', shifted)


