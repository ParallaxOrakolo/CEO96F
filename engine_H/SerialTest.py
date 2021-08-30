import FastFunctions as Fast
from time import sleep
from serial.tools import list_ports
import re
import subprocess

    
# all_port_tuples = list_ports.comports()

# print(all_port_tuples)
# #_,_,arduino = Fast.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')
Fast.validadeUSBSerial("Json/serial.json")
_,_, nano = Fast.SerialConnect(SerialPath='Json/serial.json', name='Nano')


echo = Fast.sendGCODE(nano, 'F', echo=True)

def verificaCLP(serial):
    echo = Fast.sendGCODE(serial, 'F', echo=True)
    echo = str(echo[len(echo)-1])
    print("Echo >>>", echo)
    if echo != "ok":
        try:
            return int(echo)
        except ValueError:
            return echo
        

while True:
    verificaCLP(nano)
    sleep(0.2)

# for ap, _, __ in all_port_tuples:
#     print(ap, _, __)