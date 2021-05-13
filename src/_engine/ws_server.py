import asyncio
import websockets
import json

operation = {
    "operation": {
        "name": "sc",
        "type": "simplex",
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
        "Peça com rebarba"
    ]
}

stopReasonsList = [

]

statistics = {
    "statistics": {
        "version": {
            "backend": "0.1.0"
        }
    }
}

configuration = {
    "configuration":{
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
    await ws_connection.send(json.dumps(ws_message))
    print("Enviado: " + json.dumps(ws_message))


async def startAutoCheck():
    global connection, ws_connection

    print("função start iniciada...")
    await asyncio.sleep(1)
    await ws_connection.send(json.dumps(connection))

    await asyncio.sleep(1)
    connection["connectionStatus"] = "Checando iluminação"
    await sendWsMessage("update", connection)

    await asyncio.sleep(1)
    connection["connectionStatus"] = "Verificando precisão"
    await sendWsMessage("update", connection)

    await asyncio.sleep(1)
    connection["connectionStatus"] = "Analize completa"
    await sendWsMessage("update", connection)

    await sendWsMessage("update", stopReasons)
    await sendWsMessage("update", statistics)

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
    await asyncio.sleep(1)
    await sendWsMessage("startProcess_success")

    await asyncio.sleep(2)
    operation["operation"]["placed"] = operation["operation"]["placed"] + 1
    print(operation["operation"]["placed"])
    await sendWsMessage("update", operation)
    await asyncio.sleep(2)
    operation["operation"]["placed"] = operation["operation"]["placed"] + 1
    await sendWsMessage("update", operation)

    return


async def pauseProcess():
    print("função pause process...")
    await asyncio.sleep(1)
    await sendWsMessage("pauseProcess_success")
    return


async def stopProcess():
    print("função stop process...")
    await asyncio.sleep(1)
    await sendWsMessage("stopProcess_success")
    return


async def restartProcess():
    print("função restart process...")
    await asyncio.sleep(1)

    operation["operation"]["placed"] = 0
    await sendWsMessage("update", operation)

    await sendWsMessage("restartProcess_success")
    return

async def stopReasonsResponse(obj):
    print("função stop reasons response...")
    await asyncio.sleep(1)
    stopReasonsList.append(obj)
    await sendWsMessage("stopReasonsResponse_success")
    print("segue lista de parametros")
    print(stopReasonsList)
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


async def echo(websocket, path):
    global ws_connection
    ws_connection = websocket
    async for message in ws_connection:
        print(json.loads(message))
        await actions(json.loads(message))

        # print("qual vai ser o comando?")
        # x = input()
        # await websocket.send(x)


asyncio.get_event_loop().run_until_complete(
    # websockets.serve(echo, '192.168.100.99', 443))
    websockets.serve(echo, '192.168.1.38', 5021))

print("server iniciado em ws://localhost:8765")

asyncio.get_event_loop().run_forever()
