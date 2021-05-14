import asyncio
import websockets
import json

operation = {
    "operation": {
        "name": "lc",
        "type": "duplex",
        "panel": "rodson",
        "timeSeconds": 300,
        "total": 40,
        "placed": 0,
    },
}

stopReasons = {
    "stopReasons": [
        "Conector mal encaixado",
        "Pinça soltou o conector",
        "Peça com rebarba",
        "Outros"
    ]
}

logList = {
    "log" : [
                {'code': 504,'description': 'Programa foi iniciado', 'date': 1611127092}, 
            ]
}


configuration = {
    "configuration":{
        
        "informations": {
        "ip":"192.168.100.113",
        "connectionId" : 123456,
        "port":443, 
        "version": {
            "backend": "0.1.0",
            "frontend": "0.1.1",
            "marlin": "2.0.0" #pegar automaticamente
        },
        "machine":{
            "limits" : {
                "xMin": 0,
                "yMin": 0,
                "zMin": 0,
                "aMin": -24,
                "bMin": 0,
                "xMax" : 720,
                "yMax" : 1200,
                "zMax" : 15,
                "aMax" : 11,
                "bMax" : -270,
            },
            "maxFeedrate" : {
                "xyMax" : 5000,
                "zMax" : 500,
                "aMax" : 100,
                "bMax" : 100,
            },
        },
        "userList" : [
        {
          "name": "Gabriel Palmas",
          "id": 1234,
          "lastAcess": None,
        },
         {
          "name": "Rodrigo Gomes",
          "id": 4321,
          "lastAcess": None,
        },
        {
          "name": "Arthur",
          "id": 6666,
          "lastAcess":None,
        },
        {
          "name": "Henrique",
          "id": 5678,
          "lastAcess":None ,
        } 
        ]
         },
     "statistics":{
            "stopReasonsList" : [
                {'reason': 'Conector mal encaixado', 'date': 1611127092}, 
                {'reason': 'Peça com rebarba', 'date': 1611128100}, 
                {'reason': 'Pinça soltou o conector', 'date': 1611177100}
            ],
        },
    }
}

connection = {
    "connectionStatus": "Verificando conexão"
}

ws_message = {
    "command": "",
    "parameter": ""
}

ws_connection = None

async def sendWsMessage(command, parameter=None):
    global ws_message
    ws_message["command"] = command
    ws_message["parameter"] = parameter

    cover_msg = json.dumps(ws_message, indent=2) #ident deixa o objeto mostrando bonito
    await ws_connection.send(cover_msg)
    print(25*"-")
    print("Enviado: " + cover_msg)


async def startAutoCheck():
    global connection, ws_connection

    print("função start iniciada...")
    # await asyncio.sleep(1)
    await ws_connection.send(json.dumps(connection))

    # await asyncio.sleep(1)
    connection["connectionStatus"] = "Checando iluminação"
    await sendWsMessage("update", connection)

    # await asyncio.sleep(1)
    connection["connectionStatus"] = "Verificando precisão"
    await sendWsMessage("update", connection)

    # await asyncio.sleep(1)
    connection["connectionStatus"] = "Analize completa"
    await sendWsMessage("update", connection)

    await sendWsMessage("update", stopReasons)

    await sendWsMessage("update", configuration)

    await sendWsMessage("startAutoCheck_success")
    
    return


async def scanConnectors():
    global operation
    print("função scan conector...")
    await asyncio.sleep(2)
    await sendWsMessage("update", operation)
    await sendWsMessage("scanConnectors_success")
    return


async def startProcess():
    print("função start process...")
    # await asyncio.sleep(1)
    await sendWsMessage("startProcess_success")

    # await asyncio.sleep(2)
    operation["operation"]["placed"] = operation["operation"]["placed"] + 1
    print(operation["operation"]["placed"])
    await sendWsMessage("update", operation)
    # await asyncio.sleep(2)
    operation["operation"]["placed"] = operation["operation"]["placed"] + 1
    await sendWsMessage("update", operation)

    return


async def pauseProcess():
    print("função pause process...")
    #await asyncio.sleep(1)
    await sendWsMessage("pauseProcess_success")
    return


async def stopProcess():
    print("função stop process...")
    # await asyncio.sleep(1)
    await sendWsMessage("stopProcess_success")
    return


async def restartProcess():
    print("função restart process...")
    # await asyncio.sleep(1)

    operation["operation"]["placed"] = 0
    await sendWsMessage("update", operation)

    await sendWsMessage("restartProcess_success")
    return

async def stopReasonsResponse(obj):
    print("função stop reasons response...")
    # await asyncio.sleep(1)
    configuration["configuration"]["statistics"]["stopReasonsList"].append(obj)
    # stopReasonsList.append(obj)
    await sendWsMessage("stopReasonsResponse_success")
    await sendWsMessage("update", configuration)
    print("segue lista de parametros")
    print(configuration["configuration"]["statistics"]["stopReasonsList"])
    return

async def log():
    await sendWsMessage("update", logList)
    return

async def sendGcode(obj):
    print("Gcode:"+ obj)
    return

async def serialMonitor(obj):
    print("Gcode:"+ obj)
    await sendWsMessage("serialMonitor_response", "Mensagem recebida")
    return

async def erro():
    print("deu ruin")
    return


async def actions(message):
    commad = message["command"]
    if commad == "startAutoCheck":
        await startAutoCheck()
    elif commad == "scanConnectors":
        await scanConnectors()
    elif commad == "startProcess":
        await startProcess()
    elif commad == "pauseProcess":
        await startProcess()
    elif commad == "restartProcess":
        await restartProcess()
    elif commad == "stopProcess":
        await stopProcess()
    elif commad == "stopReasonsResponse":
        await stopReasonsResponse(message["parameter"])  #message["parameter"]
    elif commad == "sendGcode":
        await sendGcode(message["parameter"])  #message["parameter"]
    elif commad == "LogRequest":
        await log()
    elif commad == "serialMonitor":
        await serialMonitor(message["parameter"]) 


# async def echo(websocket, path):
#     global ws_connection
#     ws_connection = websocket
#     async for message in ws_connection:
#         print(json.loads(message))
#         await actions(json.loads(message))

#         # print("qual vai ser o comando?")
#         # x = input()
#         # await websocket.send(x)

async def echo(websocket, path):
    global ws_connection
    if path.find("/?id=") == -1:
        print('Parametro incorreto')
        print(path)
        pass
    else:
        id = path.split("=", 1)[1]
        if not id:
            print('id nulo')
            pass
        elif id != str(configuration["configuration"]["informations"]["connectionId"]):
            print('ID de dispositivo errado')
            pass
        else:
            ws_connection = websocket
            async for message in ws_connection:
                print(json.loads(message))
                await actions(json.loads(message))



asyncio.get_event_loop().run_until_complete(
    # websockets.serve(echo, '192.168.100.99', 443))
    # websockets.serve(echo, '192.168.100.101', 443))
    websockets.serve(echo, configuration["configuration"]["informations"]["ip"], configuration["configuration"]["informations"]["port"]))


print("server iniciado em: " + configuration["configuration"]["informations"]["ip"] + ":" + str(configuration["configuration"]["informations"]["port"]))

asyncio.get_event_loop().run_forever()
