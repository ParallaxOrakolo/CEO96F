import FastFunctions as Fast
from random import choice, randint
from time import sleep
status, code, arduino = Fast.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')
ice =['-', '']
cord = [0, 270]
limit = [cord[0], cord[1]]
c = -10
Fast.sendGCODE(arduino, "G28 X")
Fast.sendGCODE(arduino, "G28 Y")
Fast.sendGCODE(arduino, "G90")
Fast.G28(arduino, offset=-28)
#Fast.sendGCODE(arduino, "G0 X 10 Y 10 F1000")
Fast.sendGCODE(arduino, "G91")
while True:
    Fast.sendGCODE(arduino, "G0 E90 F10000")
    sleep(1.6)
exit()
Teste =  "C"
speed = 10000
if Teste == "A":
    while True:
        for _ in range (0,2):
            print(f"G0 X{limit[_]} f{speed}", end=" ")
            Fast.sendGCODE(arduino, f"G0 X{limit[_]} f{speed}")
            Fast.M400(arduino)
            sleep(0.2)
        print('')
        if (limit[0] >= cord[1]) or (limit[0] <= cord[0]):
            sleep(2)
            c *= -1

        limit[0] += c
        limit[1] -= c
elif Teste == "B":
    while True:
        for x in range(randint(0, 5)):
            print(f"G0 X{choice(ice)}{randint(x, x*100)} f{speed}")
            Fast.sendGCODE(arduino, f"G0 X{choice(ice)}{randint(x, x*100)} f{speed}")
            Fast.M400(arduino)
            sleep(0.2)
elif Teste =="C":
    while True:
        print(Fast.M119(arduino)["filament"])