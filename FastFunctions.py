from time import sleep
import serial
import json
import sys


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
