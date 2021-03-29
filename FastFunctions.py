import json
from time import sleep


def readJson(json_to_read):
    with open(json_to_read, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def writeJson(json_local_save, json_data ):
    with open("json_local_save", "w", encoding='utf-8') as jsonFile:
        json.dump(json_data, jsonFile, indent=4)


def sendGCODE(serial, command, **kargs):
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
