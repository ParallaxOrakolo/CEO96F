from time import sleep
import timeit
import numpy as np
import serial
import json
import sys
import os

import string
from random import choice
from colorutils import Color

def removeEmptyFolders(path, removeRoot=True):
  if not os.path.isdir(path):
    return

  # remove empty subfolders
  files = os.listdir(path)
  if len(files):
    for f in files:
      fullpath = os.path.join(path, f)
      if os.path.isdir(fullpath):
        removeEmptyFolders(fullpath)

  # if folder empty, delete it
  files = os.listdir(path)
  if len(files) == 0 and removeRoot:
    #print ("Removing empty folder:", path)
    os.rmdir(path)

def randomString(tamanho=20, pattern=''):
    valores = string.ascii_letters + string.digits
    word = ''
    for i in range(tamanho):
        word += choice(valores)
    return pattern+word


def Hex2HSVF(hexc, rd=3, **kargs):
    CV_Range = [[0.0, 360.0],[0.0, 255],[0.0, 255]]
    Hex_Range = [[0.0, 360.0],[0.0, 1.0],[0.0, 1.0]]
    Output = []
    c = Color(hex=hexc)
    for  index in range(len(c.hsv)):
        OldValue = c.hsv[index] 
        NewValue = (((OldValue - Hex_Range[index][0]) * (CV_Range[index][1] - CV_Range[index][0])) / (Hex_Range[index][1] - Hex_Range[index][0])) + CV_Range[index][0]
        if kargs.get("prints"):
            print(f"[{c.hex}][{index}]:",OldValue,"->", NewValue)
        if rd <= 0:
            NewValue = int( round(NewValue, rd))
        else:
            NewValue = round(NewValue, rd)
        Output.append(NewValue)        
    if kargs.get("print"):
        print(hexc, '->', c.hsv, '->', Output)
    return Output


def HSVF2Hex(hsvfc, rd=5, **kargs):
    Hex_Range = [[0.0, 360.0],[0.0, 255],[0.0, 255]]
    CV_Range = [[0.0, 360.0],[0.0, 1.0],[0.0, 1.0]]
    Output = []
    c = tuple(hsvfc)
    for  index in range(len(c)):
        OldValue = c[index] 
        NewValue = (((OldValue - Hex_Range[index][0]) * (CV_Range[index][1] - CV_Range[index][0])) / (Hex_Range[index][1] - Hex_Range[index][0])) + CV_Range[index][0]
        if kargs.get("prints"):
            print(f"[{c.hex}][{index}]:",OldValue,"->", NewValue)
        if rd <= 0:
            NewValue = int( round(NewValue, rd))
        else:
            NewValue = round(NewValue, rd)
        Output.append(NewValue)        
    Output = tuple(Output)
    if kargs.get("print"):
        print(hsvfc, '->', Output, '->', Color(hsv=Output).hex)
    return Color(hsv=Output).hex

# Define cores e Tags para tratamento de exce????es.
class ColorPrint:
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    WARNING = '\033[93m'+'[Aviso]: '+'\033[0m'
    ERROR =   '\033[91m'+'[Erro]:  '+'\033[0m'
    HINT =    '\033[96m'+'[Dica]:  '+'\033[0m'
    UNDERLINE = '\033[4m'
    HEADER = '\033[95m'
    BOLD = '\033[1m'

class MyException(Exception):
    pass
# Cria uma imagem de cor solida com qualquer tamanho,, padr??o 600x900 azul
def backGround(h=600, w=900, c=0):
    bgk = np.zeros([h, w, 3], np.uint8)
    bgk[:, :, c] = np.zeros([h, w]) + 255
    return bgk

# Abre e l?? um json no caminho solicitado.
def readJson(json_to_read):
    if os.path.exists("engine/"):
        prefix = "engine/"
    else:
        prefix=""
    with open(f"{prefix}{json_to_read}", 'r', encoding='utf8') as json_file:
        return json.load(json_file)


# Abre e grava um json no caminho solicitado.
def writeJson(json_local_save, json_data):
    if os.path.exists("engine/"):
        prefix = "engine/"
    else:
        prefix=""
    with open(f"{prefix}{json_local_save}", "w", encoding='utf8') as jsonFile:
        json.dump(json_data, jsonFile, indent=4, ensure_ascii=False)


# Envia um ou uma lista de comandos na serial, se poss??vel e se requisitado retorna a resposta.
def sendGCODE(serial, command, **kargs):
    # Verifica se ?? possivel enviar dados atrav??s da conex??o informada.
    if serial and type(serial) not in [tuple, str, int, bool]:
        
        # Garante que os motores estar??o travados
#        serial.write(str("M17 X Y Z E" + '{0}'.format('\n')).encode('ascii'))
        # log = open('logMarlin.txt', 'a')
        #     #f.write(serial)
        # if command != 'F':
        #     log.write(f"{command} \n")
        # log.close()
        # Limpa o buffer.
        serial.flush()
        serial.flushInput()
        serial.flushOutput()

        # Verifica se ?? um unico comando
        if isinstance(command, str):
            serial.write(str(command + '{0}'.format('\n')).encode('ascii'))
        # Verifica se ?? uma lista de comandos
        if isinstance(command, list):
            for linha in command:
                serial.write(str(linha + '{0}'.format('\n')).encode('ascii'))

        # Verifica se ?? uma lista de comandos do tipo "dicion??rio".
        if isinstance(command, dict):
            for linha in command:
                serial.write(str(command[linha] + '{0}'.format('\n')).encode('ascii'))

        # Espera por algum retorno
        tt = timeit.default_timer()
        while timeit.default_timer() - tt <=0.1:
            continue
        #sleep(0.1)
        strr = []

        # L??, decodifica e processa enquanto houver informa????o no buffer de entrada.
        echo0 = timeit.default_timer()
        while True:
            b = serial.readline()
            string_n = b.decode()
            strr.append(string_n.rstrip())
            if b == b'':
                print("b:", b, type(b))
                print("string_n:", string_n, type(string_n))
                print("string_n.rstrip():", string_n.rstrip(), type(string_n.rstrip()))
                break
            if serial.inWaiting() == 0:
                break
            # elif timeit.default_timer() - echo0 >= 5:
            #     raise MyException(f"Comando enviado, mas nenhuma resposta foi obtida, desconecte e reconecte a porta serial")
        if b == b'' or b == None or b is None:
            raise MyException("Conex??o com placa foi encontrada, mas ela n??o responde...")
        # Se requisitado, retorna aquilo que foi recebido ap??s o envio dos comandos.
        if kargs.get('echo'):
            return strr

        # Limpa o buffer.
        serial.flush()
        serial.flushInput()
        serial.flushOutput()

    # Avisa que o comando n??o pode ser enviado, pois a conex??o n??o existe.
    else:
        return ["Comando n??o enviado, falha na conex??o com a serial."]


def M114(serial, type='', where=[("X:", " Y:"), ("Y:", " Z:"), ("Z:", " A:"), ("A:", " Count")]):
    for _ in range(2):
        Echo = (sendGCODE(serial, f"M114 {type}", echo=True))[0]
    try:
        Pos = []
        for get in where:
            left, right = get[0], get[1]
            Pos.append(float(Echo[Echo.index(left)+len(left):Echo.index(right)]))
        return dict(zip(['X', 'Y', 'Z', 'A'], Pos))
    except ValueError:
        print("Recebi:", Echo)
        return Echo

def M115(serial, line=0, start=21, end=28):
    return sendGCODE(serial, "M115", echo=True)[line][start:end]

def M119(serial, cut=": "):
    pos=[]
    key=[]
    #for _ in range(2):
    Echo = (sendGCODE(serial, "M119", echo=True))[1:-1]
        #print(Echo)
    for info in Echo:
        try:
            pos.append(info[info.index(cut)+len(cut):len(info)])
            key.append(info[0:info.index(cut)])
        except ValueError:
            print("ERRO:", info)
    return dict(zip(key, pos))


def G28(serial, axis='E', endStop='filament', status='open',offset=-23, steps=5, speed=50000):
    sendGCODE(serial, "G91")
    while True:
        try:
            if M119(serial)[endStop] != status:
                sendGCODE(serial, f"G0 E{offset * -1} F{speed}")
            break
        except KeyError:
            pass

    while True:
        try:
            while M119(serial)[endStop] == status:
                sendGCODE(serial, f"G0 {axis}{steps} F{speed}")

            sendGCODE(serial, "G91")
            sendGCODE(serial, f"G0 E-{10} F{speed}")

            while M119(serial)[endStop] == status:
                sendGCODE(serial, f"G0 {axis}{1} F{speed}")

            sendGCODE(serial, "G91")
            sendGCODE(serial, f"G0 E{offset} F{speed}")
            #sendGCODE(serial, f"G92 E0")
            sendGCODE(serial, "G90")
            break
        except KeyError:
            pass
    


def M400(arduino, pattern='', **kwargs):
    echoMessge, echoCaugth = " ", ['x', 'X']
    timeout= kwargs.get('timeout') if kwargs.get('timeout') else 20
    T0 = timeit.default_timer()
    while echoMessge not in echoCaugth:
        if timeit.default_timer() - T0 <= timeout:
            echoMessge = pattern+'_'+randomString()
            echoCaugth = sendGCODE(arduino, "M400",  echo=True)
            echoCaugth += sendGCODE(arduino, f"M118 {echoMessge}", echo=True)
        else:
            print("Saiu m400")
            raise MyException(f"Movimento n??o pode ser concluido dentro de {timeout} segundos.")


def MoveTo(arduino, *args, **kargs):
    cords = ""
    for pos in args:
        axis = pos[0].upper()
        pp = pos[1]
        cords+=f"{axis}{pp} "
    sendGCODE(arduino, f"G0 {cords}")
    if kargs.get("nonSync"):
        return
    futuro = M114(arduino)
    real = M114(arduino, 'R')
    #while True:
    a = [v for v in futuro.values()]
    b = [v for v in real.values()]
    while not all((a[i] - 0.5 <= b[i] <= a[i] + 0.5) == True for i in range(len(b))):
        real = M114(arduino, 'R')
        b = [v for v in real.values()]
        #print(a, b)
        
    real = M114(arduino, 'R')
    #print(real, futuro)
    pass

# Estabelece uma conex??o com base em um arquivo de configura????o personalizado.
def SerialConnect(SerialPath='../Json/serial.json', name='arduino'):
    if os.path.exists("engine/"):
        SerialPath='engine/Json/serial.json'
    # Tenta Estabelecer uma conex??o.
    try:
        with open(SerialPath, 'r', encoding='utf-8') as serial_json_file:
            serialData = json.load(serial_json_file)
        communication = serial.Serial(serialData[name]['porta'], serialData[name]['velocidade'], timeout=3)

    # Conex??o falhou porque o arquivo de configura????o n??o foi encontrado.
    except FileNotFoundError:
        print(f"{ColorPrint.ERROR}O argumento [SerialPath='{SerialPath}'] ?? inv??lido.")
        return False, -1, "Caminho especificado para conex??o n??o pode ser encontrado."
        sys.exit(-1)

    # Conex??o falhou porque o nome da conex??o ??o existe no arquivo de configura????o.
    except KeyError as Ker:
        print(f"{ColorPrint.ERROR}O argumento [name='{name}'] ?? inv??lido.")
        return False, -2, "Identificador para conex??o n??o existe."

    # Conex??o foi estabelecida, mas caiu.
    except serial.serialutil.SerialException as Erro_Conexao:
        print(f"{ColorPrint.ERROR}N??o foi possivel estabelecer uma conex??o com [{name}].")

        # Conex??o n??o se manteve, ap??s a tentativa porque n??o h?? nada ao que se conectar.
        if "FileNotFoundError" in str(Erro_Conexao):
            print(f"{ColorPrint.WARNING}Verifique a porta [{serialData[name]['porta']}]"'\n')
            return False, -3, "N??o foi possivel estabelecer conex??o com o controlador."
        # Conex??o n??o se manteve, ap??s a tentativa porque h?? porta j?? est?? possui uma conex??o.
        elif 'Acesso negado.' in str(Erro_Conexao):
            print(f"{ColorPrint.WARNING}A porta [{serialData[name]['porta']}] est?? ocupada."'\n')
            return False, -4, "Porta do controlador j?? se encontra em uso, feche as demais conex??es."
    # Conex??o foi estabelecida com sucesso.
    else:
        print(
            f"{ColorPrint.CYAN}[{serialData[name]['porta']} - OK]: Conex??o com [{name}] estabelecida."
            f"{ColorPrint.ENDC}"'\n'
        )

        # Espera para que a conex??o se estabiliza.
        sleep(1.2)

        return True, 200, communication


def validadeUSBSerial(SerialPath):
    serialPack = readJson(SerialPath)
    changes = [{"id":"none", "porta":"None"}]
    for k, v in serialPack.items():
        try:
            _,_, serial = SerialConnect(SerialPath=SerialPath, name=k)
            message = serial.readline().decode().rstrip()
            if str(message) != v["expectedMessage"] and message != "" and message is not None:
                print("Erro", k, message)
                for k2, v2 in serialPack.items():
                    if v2["expectedMessage"] == message:
                        v["porta"], v2["porta"] = v2["porta"], v["porta"]
                        #v["expectedMessage"], v2["expectedMessage"] = v2["expectedMessage"], v["expectedMessage"]
            serial.close()
            writeJson(SerialPath, serialPack)
        except Exception as err:
            print(err)
            pass

def EditJson(org, org_path, chg, chg_path='["configuration"]["informations"]["ip"]'):

    # lista ='["configuration"]["informations"]["ip"]'
    a = eval(str(org)+org_path)
    b = eval(str(chg)+chg_path+' = '+a)
    print(a)
    print(b)

