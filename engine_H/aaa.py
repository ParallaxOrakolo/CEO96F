def mm2coordinate(x, c=160, aMin=148.509, reverse=False):
    if not reverse:
        r = aMin-(c**2 - ((c**2-aMin**2)**0.5+x)**2)**0.5
 #       edit(f"Convertendo {x} em {r} | reverse=False\n")
        return r
    else:
        r = ((c**2 - (aMin-x)**2)**0.5)-(c**2 - aMin**2)**0.5
#        edit(f"Convertendo {x} em {r} | reverse=True\n")
        return r

import FastFunctions as Fast
def RAIZ(x):
    return x**0.5
arduino=2
def mm2coordinate(Variacao = 0, m114=0, hipotenusa = 160, aberturaMinima = 149.509, simul=False):
    if not simul:
        coordenadaAtual_A = (aberturaMinima - Fast.M114(arduino)['Y'])
    else:
        coordenadaAtual_A = (aberturaMinima - m114)
    a = RAIZ(hipotenusa**2 - (RAIZ(hipotenusa**2-coordenadaAtual_A**2)+Variacao)**2)
    print(a, aberturaMinima-a)
    return aberturaMinima-a

while True:

    print(F'G0 Y{mm2coordinate(float(input("mm:")), float(input("cc:")), simul=True)} F5000')
# Fast.validadeUSBSerial('Json/serial.json')
# status, code, arduino = Fast.SerialConnect(
                # SerialPath='Json/serial.json', name='Ramps 1.4')

# Fast.sendGCODE(arduino, 'G28 Y')
# Fast.sendGCODE(arduino, 'G28 X')
# Fast.sendGCODE(arduino, 'G0 X200 F5000')
# Fast.sendGCODE(arduino, 'G90')
# Fast.sendGCODE(arduino, 'G0 Y10')
# while True:
#     Fast.sendGCODE(arduino, F'G0 Y{A2B(float(input("mm:")))} F5000')


# 4.58 --- 0.0
# 3.38     4.103
10.5