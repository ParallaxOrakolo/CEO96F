from time import sleep
import numpy as np
import serial
import json
import sys

import string
from random import choice

def randomString(tamanho=20, pattern=''):
    valores = string.ascii_letters + string.digits
    word = ''
    for i in range(tamanho):
        word += choice(valores)
    return pattern+word


# Define cores e Tags para tratamento de exceções.
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

# Cria uma imagem de cor solida com qualquer tamanho,, padrão 600x900 azul
def backGround(h=600, w=900, c=0):
    bgk = np.zeros([h, w, 3], np.uint8)
    bgk[:, :, c] = np.zeros([h, w]) + 255
    return bgk

# Abre e lê um json no caminho solicitado.
def readJson(json_to_read):
    with open(json_to_read, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


# Abre e grava um json no caminho solicitado.
def writeJson(json_local_save, json_data):
    with open(json_local_save, "w", encoding='utf-8') as jsonFile:
        json.dump(json_data, jsonFile, indent=4)


# Envia um ou uma lista de comandos na serial, se possível e se requisitado retorna a resposta.
def sendGCODE(serial, command, **kargs):
    # Verifica se é possivel enviar dados através da conexão informada.
    if serial:

        # Limpa o buffer.
        serial.flush()
        serial.flushInput()
        serial.flushOutput()

        # Verifica se é um unico comando
        if isinstance(command, str):
            serial.write(str(command + '{0}'.format('\n')).encode('ascii'))

        # Verifica se é uma lista de comandos
        if isinstance(command, list):
            for linha in command:
                serial.write(str(linha + '{0}'.format('\n')).encode('ascii'))

        # Verifica se é uma lista de comandos do tipo "dicionário".
        if isinstance(command, dict):
            for linha in command:
                serial.write(str(command[linha] + '{0}'.format('\n')).encode('ascii'))

        # Espera por algum retorno
        sleep(0.1)
        strr = []

        # Lê, decodifica e processa enquanto houver informação no buffer de entrada.
        while True:
            b = serial.readline()
            string_n = b.decode()
            strr.append(string_n.rstrip())
            if serial.inWaiting() == 0:
                break

        # Se requisitado, retorna aquilo que foi recebido após o envio dos comandos.
        if kargs.get('echo'):
            return strr

        # Limpa o buffer.
        serial.flush()
        serial.flushInput()
        serial.flushOutput()

    # Avisa que o comando não pode ser enviado, pois a conexão não existe.
    else:
        return ["Comando não enviado..."]


def M114(serial, where=[("X:", " Y:"), ("Y:", " Z:"), ("Z:", " E:"), ("E:", " Count")]):
    for _ in range(2):
        Echo = (sendGCODE(serial, "M114", echo=True))[0]
    try:
        Pos = []
        for get in where:
            left, right = get[0], get[1]
            Pos.append(float(Echo[Echo.index(left)+len(left):Echo.index(right)]))
        return dict(zip(['X', 'Y', 'Z', 'E'], Pos))
    except ValueError:
        print("Recebi:", Echo)
        return Echo

def M119(serial, cut=": "):
    pos=[]
    key=[]
    for _ in range(2):
        Echo = (sendGCODE(serial, "M119", echo=True))[1:-1]
        print(Echo)
    for info in Echo:
        pos.append(info[info.index(cut)+len(cut):len(info)])
        key.append(info[0:info.index(cut)])
    return dict(zip(key, pos))

def G28(serial, axis='E', endStop='filament', status='open', steps=5, speed=50000):
    sendGCODE(serial, "G91")
    while M119(serial)[endStop] == status:
        sendGCODE(serial, f"G0 {axis}{steps} F{speed}")
    sendGCODE(serial, "G90")

def M400(arduino, pattern='', **kwargs):
    echoMessge, echoCaugth = " ", ['x', 'X']
    while echoMessge not in echoCaugth:
        echoMessge = pattern+'_'+randomString()
        echoCaugth = sendGCODE(arduino, "M400",  echo=True)
        echoCaugth += sendGCODE(arduino, f"M118 {echoMessge}", echo=True)

# Estabelece uma conexão com base em um arquivo de configuração personalizado.
def SerialConnect(SerialPath='../Json/serial.json', name='arduino'):
    # Tenta Estabelecer uma conexão.
    try:
        with open(SerialPath, 'r', encoding='utf-8') as serial_json_file:
            serialData = json.load(serial_json_file)
        communication = serial.Serial(serialData[name]['porta'], serialData[name]['velocidade'])

    # Conexão falhou porque o arquivo de configuração não foi encontrado.
    except FileNotFoundError:
        print(f"{ColorPrint.ERROR}O argumento [SerialPath='{SerialPath}'] é inválido.")
        sys.exit(-1)

    # Conexão falhou porque o nome da conexão ão existe no arquivo de configuração.
    except KeyError as Ker:
        print(f"{ColorPrint.ERROR}O argumento [name='{name}'] é inválido.")
        sys.exit(-1)

    # Conexão foi estabelecida, mas caiu.
    except serial.serialutil.SerialException as Erro_Conexao:
        print(f"{ColorPrint.ERROR}Não foi possivel estabelecer uma conexão com [{name}].")

        # Conexão não se manteve, após a tentativa porque não há nada ao que se conectar.
        if "FileNotFoundError" in str(Erro_Conexao):
            print(f"{ColorPrint.WARNING}Verifique a porta [{serialData[name]['porta']}]"'\n')

        # Conexão não se manteve, após a tentativa porque há porta já está possui uma conexão.
        elif 'Acesso negado.' in str(Erro_Conexao):
            print(f"{ColorPrint.WARNING}A porta [{serialData[name]['porta']}] está ocupada."'\n')

        return False

    # Conexão foi estabelecida com sucesso.
    else:
        print(
            f"{ColorPrint.CYAN}[{serialData[name]['porta']} - OK]: Conexão com [{name}] estabelecida."
            f"{ColorPrint.ENDC}"'\n'
        )

        # Espera para que a conexão se estabiliza.
        sleep(1.2)

        return communication
