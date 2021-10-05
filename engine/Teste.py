import FastFunctions as Fast
from random import choice, randint
from time import sleep
status, code, arduino = Fast.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')
