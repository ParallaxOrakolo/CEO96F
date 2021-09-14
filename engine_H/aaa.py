import FastFunctions as Fast
from random import choice, randint
from time import sleep
status, code, arduino = Fast.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')
Fast.sendGCODE(arduino, 'g91')
Fast.sendGCODE(arduino, 'G0 z-10')
#Fast.sendGCODE(arduino, 'G28 xya')
Fast.sendGCODE(arduino, 'G28 y')
#Fast.sendGCODE(arduino, "G0 X260 F10000")
#Fast.sendGCODE(arduino, 'G28 Z')
#Fast.sendGCODE(arduino, 'G0 z150 f5000')
Fast.sendGCODE(arduino, "M201 Y50")
Fast.sendGCODE(arduino, "M500")
Fast.M400(arduino)
Fast.sendGCODE(arduino,'G90')
list = [
"g0 Y39.37 F45600",
"G0 Y5.22 F45600",
"g0 Y39.37 F45600"]

listSSSSS = [
"g0 Y39.94 F4500",
"G0  Y5.22 E180 F4500",
"g0 Y39.37 F4500"]
#"G0 X271.55 Y15.22 E180 F500", DEU CERTO
#"M43 T S33 L33 R3 W100", FALHOU
#"g0 Y40.37 X264.10 F5600",
listss = [
"g0 Y40.943200000000004 X241.5007 F5600",
"G0 X261.5587 Y5.2203 E180 F5600",
"g0 Y40.3744 X264.1076 F5600"]
lista = [
"G0 X239.3143 Y5.3012 E0 F5600",
"g0 Y40.943200000000004 X241.5007 F5600",

"G0 X261.5587 Y5.2203 E180 F5600",
"00000000004 X264.1076 F5600",

"G0 X236.6319 Y5.4019 E270 F5600",
"g0 Y40.5915 X236.4469 F5600",

"G0 X262.4323 Y5.4783 E270 F5600",

"G0 X239.3143 Y5.3012 E0 F5600",
"g0 Y40.664100000000005 X244.7108 F5600",

"G0 X261.5587 Y5.2203 E180 F5600",
"g0 Y40.4632 X267.5766 F5600",

"G0 X236.6319 Y5.4019 E270 F5600 ",
"G0 X262.4323 Y5.4783 E270 F5600",

"G0 X239.3143 Y5.3012 E0 F5600",
"g0 Y40.6205 X244.8457 F5600",

"G0 X261.5587 Y5.2203 E180 F5600",
"g0 Y40.357600000000005 X267.2961 F5600",

"G0 X236.6319 Y5.4019 E270 F5600"]

for item in list:
    Fast.sendGCODE(arduino, item)
    Fast.M400(arduino)
    sleep(2)

exit()