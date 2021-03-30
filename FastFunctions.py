from time import sleep
import serial
import json
import sys


class ColorPrint:
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    WARNING = '\033[93m'+'[Aviso]: '+'\033[0m'
    ERROR =   '\033[91m'+'[Erro]:  '+'\033[0m'

    UNDERLINE = '\033[4m'
    HEADER = '\033[95m'
    BOLD = '\033[1m'


def readJson(json_to_read):
    with open(json_to_read, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def writeJson(json_local_save, json_data ):
    with open("json_local_save", "w", encoding='utf-8') as jsonFile:
        json.dump(json_data, jsonFile, indent=4)


def sendGCODE(serial, command, **kargs):
    if serial:
        serial.flush()
        serial.flushInput()
        serial.flushOutput()
        if isinstance(command, str):
            serial.write(str(command + '{0}'.format('\n')).encode('ascii'))

        if isinstance(command, list):
            for linha in command:
                serial.write(str(linha + '{0}'.format('\n')).encode('ascii'))

        if isinstance(command, dict):
            for linha in command:
                serial.write(str(command[linha] + '{0}'.format('\n')).encode('ascii'))

        sleep(0.1)
        strr = []
        while True:
            b = serial.readline()
            string_n = b.decode()
            strr.append(string_n.rstrip())
            if serial.inWaiting() == 0:
                break

        if kargs.get('echo'):
            return strr

        serial.flush()
        serial.flushInput()
        serial.flushOutput()
    else:
        return ["Comando não enviado..."]


def SerialConnect(SerialPath='../Json/serial.json', name='arduino'):
    try:
        with open(SerialPath, 'r', encoding='utf-8') as serial_json_file:
            serialData = json.load(serial_json_file)
        communication = serial.Serial(serialData[name]['porta'], serialData[name]['velocidade'])

    except FileNotFoundError:
        print(f"{ColorPrint.ERROR}O argumento [SerialPath='{SerialPath}'] é inválido.")
        sys.exit(-1)

    except KeyError as Ker:
        print(f"{ColorPrint.ERROR}O argumento [name='{name}'] é inválido.")
        sys.exit(-1)

    except serial.serialutil.SerialException as Erro_Conexao:
        print(f"{ColorPrint.ERROR}Não foi possivel estabelecer uma conexão com [{name}].")
        if "FileNotFoundError" in str(Erro_Conexao):
            print(f"{ColorPrint.WARNING}Verifique a porta [{serialData[name]['porta']}]"'\n')
        elif 'Acesso negado.' in str(Erro_Conexao):
            print(f"{ColorPrint.WARNING}A porta [{serialData[name]['porta']}] está ocupada."'\n')
        return False
    else:
        print(
            f"{ColorPrint.CYAN}[{serialData[name]['porta']} - OK]: Conexão com [{name}] estabelecida."
            f"{ColorPrint.ENDC}"'\n'
        )

        sleep(1.2)
        return communication
