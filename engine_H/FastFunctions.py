from time import sleep
import timeit
import numpy as np
import serial
import json
import sys
import os

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

class MyException(Exception):
    pass
# Cria uma imagem de cor solida com qualquer tamanho,, padrão 600x900 azul
def backGround(h=600, w=900, c=0):
    bgk = np.zeros([h, w, 3], np.uint8)
    bgk[:, :, c] = np.zeros([h, w]) + 255
    return bgk

# Abre e lê um json no caminho solicitado.
def readJson(json_to_read):
    if os.path.exists("engine_H/"):
        prefix = "engine_H/"
    else:
        prefix=""
    with open(f"{prefix}{json_to_read}", 'r', encoding='utf8') as json_file:
        return json.load(json_file)


# Abre e grava um json no caminho solicitado.
def writeJson(json_local_save, json_data):
    if os.path.exists("engine_H/"):
        prefix = "engine_H/"
    else:
        prefix=""
    with open(f"{prefix}{json_local_save}", "w", encoding='utf8') as jsonFile:
        json.dump(json_data, jsonFile, indent=4, ensure_ascii=False)


# Envia um ou uma lista de comandos na serial, se possível e se requisitado retorna a resposta.
def sendGCODE(serial, command, **kargs):
    # Verifica se é possivel enviar dados através da conexão informada.
    if serial and type(serial) not in [tuple, str, int, bool]:

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
            raise MyException("Conexão com placa foi encontrada, mas ela não responde...")
        # Se requisitado, retorna aquilo que foi recebido após o envio dos comandos.
        if kargs.get('echo'):
            return strr

        # Limpa o buffer.
        serial.flush()
        serial.flushInput()
        serial.flushOutput()

    # Avisa que o comando não pode ser enviado, pois a conexão não existe.
    else:
        return ["Comando não enviado, falha na conexão com a serial."]


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
            raise MyException(f"Movimento não pode ser concluido dentro de {timeout} segundos.")

# Estabelece uma conexão com base em um arquivo de configuração personalizado.
def SerialConnect(SerialPath='../Json/serial.json', name='arduino'):
    if os.path.exists("engine_H/"):
        SerialPath='engine_H/Json/serial.json'
    # Tenta Estabelecer uma conexão.
    try:
        with open(SerialPath, 'r', encoding='utf-8') as serial_json_file:
            serialData = json.load(serial_json_file)
        communication = serial.Serial(serialData[name]['porta'], serialData[name]['velocidade'], timeout=3)

    # Conexão falhou porque o arquivo de configuração não foi encontrado.
    except FileNotFoundError:
        print(f"{ColorPrint.ERROR}O argumento [SerialPath='{SerialPath}'] é inválido.")
        return False, -1, "Caminho especificado para conexão não pode ser encontrado."
        sys.exit(-1)

    # Conexão falhou porque o nome da conexão ão existe no arquivo de configuração.
    except KeyError as Ker:
        print(f"{ColorPrint.ERROR}O argumento [name='{name}'] é inválido.")
        return False, -2, "Identificador para conexão não existe."

    # Conexão foi estabelecida, mas caiu.
    except serial.serialutil.SerialException as Erro_Conexao:
        print(f"{ColorPrint.ERROR}Não foi possivel estabelecer uma conexão com [{name}].")

        # Conexão não se manteve, após a tentativa porque não há nada ao que se conectar.
        if "FileNotFoundError" in str(Erro_Conexao):
            print(f"{ColorPrint.WARNING}Verifique a porta [{serialData[name]['porta']}]"'\n')
            return False, -3, "Não foi possivel estabelecer conexão com o controlador."
        # Conexão não se manteve, após a tentativa porque há porta já está possui uma conexão.
        elif 'Acesso negado.' in str(Erro_Conexao):
            print(f"{ColorPrint.WARNING}A porta [{serialData[name]['porta']}] está ocupada."'\n')
            return False, -4, "Porta do controlador já se encontra em uso, feche as demais conexões."
    # Conexão foi estabelecida com sucesso.
    else:
        print(
            f"{ColorPrint.CYAN}[{serialData[name]['porta']} - OK]: Conexão com [{name}] estabelecida."
            f"{ColorPrint.ENDC}"'\n'
        )

        # Espera para que a conexão se estabiliza.
        sleep(1.2)

        return True, 200, communication

def EditJson(org, org_path, chg, chg_path='["configuration"]["informations"]["ip"]'):

    # lista ='["configuration"]["informations"]["ip"]'
    a = eval(str(org)+org_path)
    b = eval(str(chg)+chg_path+' = '+a)
    print(a)
    print(b)

