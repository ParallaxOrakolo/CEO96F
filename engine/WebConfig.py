# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
# Nota: Use Crtl + Shift + -    para colapsar todo o código e facilitar a visualização.
#
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #

from flask import Flask, Response, request, jsonify
from FastFunctions import MyException
from datetime import datetime
from threading import Thread
from math import floor
from ast import literal_eval
import FastFunctions as Fast
import OpencvPlus as Op
import numpy as np
import websockets
import subprocess
import threading
import platform
import asyncio
import random
import socket
import timeit
import json
import time
import cv2
import os
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                      JSON                                                            #

ws_message = {
    "command": "",
    "parameter": ""
}

operation = {
    "operation": {
        "name": "Estribo",
        "type": "",
        "panel": "",
        "timeSeconds": 0,
        "total": 0,
        "placed": 0,
        "right": 0,
        "wrong": 0,
        "stopped": True,
        "finished": True,
        "started": False,
        "running": False,
        "onlyCorrectParts": False,
        "stopSuccess": False
    },
}



"""
    Inicia -> Escuta a conexão.

    Front incicia ->
        É a primeria vez?
            sim: Reseta as posições, incicia as threads.
            não: Avança pra tela de start?

        Botão de start precionado:
            Avisa o front.
            "CLP OK?:
                sim: roda "Processo de identificação (PI)", até o final.
                PI ok? (6 furos identificados?):
                    sim: roda "Processo de parafusar (PP)", até o final.
                         roda "Validação dos parafursos (VP)", até o final.
                         VP ok? (Tem seis parafusos?):
                            sim: larga a peça na posição certa
                            não: larga a peça na posição errada.
                            Volta pro "CPL OK".
                    não: Avisa o front. Reseta a maquina.
                não: Avisa o front. Reseta a maquina.

        Botão de parada precionado:
            Avisa o front.
            Deseja parar?:
                sim: Conclui o movimento
                     Descarta como errado
                     retrai eixo Z
                     zera Y
                     Zera X e Z
            Avisa o front.



"""
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                      Class                                                           #
class CLP(threading.Thread):
    def __init__(self, serial, interval):
        super(CLP, self).__init__()
        self.serial = serial
        self.Status_Atual = "ok"
        self.errorList = ["ok"]
        self.readInterval = interval
        self._stop_event = threading.Event()
        self._read_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def removeDuplicate(self):
        return list(dict.fromkeys(self.errorList))
    
    def getStatus(self):
        self._read_event.set()
        if self.errorList:
            self.Status_Atual = self.errorList[0]
            del self.errorList[0]
        else:
            self.Status_Atual = "ok"
        print(f"nano: get {self.Status_Atual} from {self.errorList}")
        self._read_event.clear()
        return self.Status_Atual

    def getList(self):
        return self.errorList

    def run(self):
        while not self.stopped():
            tt = timeit.default_timer()
            while timeit.default_timer() - tt <= self.readInterval:
                pass
            if not self._read_event.is_set():
                a = verificaCLP(self.serial)
                if a !=  None and a > 0:
                    self.errorList.append(a)
                self.errorList = self.removeDuplicate()
            
class Hole_Filter(threading.Thread):
    def __init__(self):
        super(Hole_Filter, self).__init__()
        self._stop_event = threading.Event()
        self.get_data = threading.Event()
        self.Mx = None
        self.My = None
        self.mmy = []
        self.mmx = []
        self.frame = None
        self.draw = None

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            self.frame =globals()['frame'+str(mainParamters["Cameras"]["hole"]["Settings"]["id"])]
            RR, _, _, self.draw = Process_Image_Hole(
                        self.frame,
                        mainParamters['Mask_Parameters']['hole']['areaMin'],
                        mainParamters['Mask_Parameters']['hole']['areaMax'],
                        mainParamters['Mask_Parameters']['hole']['perimeter'],
                        mainParamters['Filtros']['HSV']['hole']['Valores']
                    )
            if RR:
                self.mmx.append(RR[0][1])
                self.mmy.append(RR[0][0])

                while len(self.mmx) > 5:
                    self.mmx.pop(0)
                while len(self.mmy) > 5:
                    self.mmy.pop(0)

                self.Mx = sum(self.mmx)/len(self.mmx)
                self.My = sum(self.mmy)/len(self.mmy)
            else:
                self.clear()
    def clear(self):
        self.Mx = None
        self.My = None
        self.mmx = []
        self.mmy = []

    def getData(self):
        a,b,c,d = self.Mx, self.My, self.frame, self.draw
        self.clear()
        return a,b,c,d
            
            
class CamThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self._running = True

        self.Procs = {"hole": False,
                      "screw": False, "normal": False}

        self.Processos = ['screw']
        self.pFA = (50, 50)
        self.pFB = (100, 60)
        self.fixPoiint = (self.pFB[0], int(
            self.pFA[1] + ((self.pFB[1] - self.pFA[1]) / 2)))

        self._stop_event = threading.Event()
        self.get_data = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        print("Starting " + self.previewName)
        return self.camPreview(self.previewName, self.camID)

    async def report(self, item):
        item["description"] = item["description"].replace(
            "_id_", str(self.camID['Settings']['id']))
        await sendWsMessage("error", item)

    def camPreview(self, previewName, cam_json):
        # Abre a camera com o id passado.
        camID = cam_json["Settings"]["id"]
        cw = cam_json["Settings"]["frame_width"]
        ch = cam_json["Settings"]["frame_height"]
        print(cw, 'x', ch)
        cam = cv2.VideoCapture(camID)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, int(cw))
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, int(ch))
        cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        if cam.isOpened():                            # Verifica se foi aberta
            rval, frame = cam.read()                  # Lê o Status e uma imagem
        else:
            globals()[f'frame{previewName}'] = cv2.imread(
                f"../engine/Images/{camID}.jpg")
            rval = False

        while rval and not self.stopped():                                   # Verifica e camera ta 'ok'

            rval, frame = cam.read()                  # Atualiza
            frame = cv2.blur(frame, (3, 3))
            #if blurry <= 110:
            globals()[f'frame{previewName}'] = frame
            #if cv2.waitKey(1) == 27:
            #    break
        try:
            cv2.destroyWindow(previewName)
        except cv2.error:
            pass
        cam.release()
        print("Saindo da thread", self.previewName)
        infoCode = 16
        for item in stopReasons:
            if infoCode == item['code']:
                asyncio.run(self.report(item))
        return False

    def ViewCam(self):
        while not self.stopped():
            if self.Procs['screw']:

                frame, _, _ = Process_Image_Screw(
                    globals()['frame'+self.previewName],
                    Op.extractHSValue(
                        mainParamters['Filtros']['HSV']['screw']["Valores"], 'lower'),
                    Op.extractHSValue(
                        mainParamters['Filtros']['HSV']['screw']["Valores"], 'upper'),
                    mainParamters['Mask_Parameters']['screw']['areaMin'],
                    mainParamters['Mask_Parameters']['screw']['areaMax'],
                    model=modelo_atual
                )
                # _, frame = findScrew(globals()[
                #                      'frame'+self.previewName], mainParamters['Filtros']['HSV'], mainParamters, self.Processos)
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 10])[1].tobytes()
                       + b'\r\n')
            if self.Procs['hole']:
                _, _, _, frame = Process_Image_Hole(
                    globals()['frame' + self.previewName],
                    mainParamters['Mask_Parameters']['hole']['areaMin'],
                    mainParamters['Mask_Parameters']['hole']['areaMax'],
                    mainParamters['Mask_Parameters']['hole']['perimeter'],
                    mainParamters['Filtros']['HSV']['hole']['Valores']
                )
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 10])[1].tobytes()
                       + b'\r\n')
            if self.Procs['normal']:
                # print("normal")
                frame = globals()['frame'+self.previewName].copy()
                cv2.drawMarker(
                    frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)), (255, 50, 0), 0, 1000, 5)
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 10])[1].tobytes()
                       + b'\r\n')
        print("Fechando Vizualizção")


class AppThread(threading.Thread):
    def __init__(self, app_ip, app_port):
        threading.Thread.__init__(self)
        self.ip = app_ip
        self.port = app_port
        self._running = True

    def run(self):
        global StartedStream
        print("rodando....")
        app.run(host=self.ip, port=self.port, debug=True,
                threaded=True, use_reloader=False)

        StartedStream = False

        print("parou!")

    def stop(self):
        app.shutdown()
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class ViewAnother(threading.Thread):
    def __init__(self, quem, intervalo):
        threading.Thread.__init__(self)
        self.look_at = quem
        self.look_time = intervalo
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            if self.look_at.stopped():
                print("PUTZ")
            time.sleep(self.look_time)


class mediaMovel():
    def __init__(self, limite, inicializador=0):
        self.valores = [inicializador]*limite
        self.recebido = None
        self.media = None
        self.limite = limite
        self.ignore = [None]

    def atualizaVetor(self):
        if self.recebido not in self.ignore:
            self.valores.append(self.recebido)

        while len(self.valores) > self.limite:
            self.valores.pop(0)

    def atualizaMedia(self):
        if len(self.valores) >= self.limite:
            self.media = round(sum(self.valores)/len(self.valores), 4)
            return self.media
        else:
            return False


class Process(threading.Thread):
    def __init__(self, quantidad, id, model, only):
        threading.Thread.__init__(self)
        global intencionalStop, arduino, nano, infoCode
        self.qtd = quantidad
        self.corretas = 0
        self.erradas = 0
        self.rodada = 0
        self.only = only
        self.infoCode = infoCode
        # Destrava a maquina quando um novo processo é iniciado.
        intencionalStop = False
        self.arduino = arduino
        self.nano = nano
        self.model = model
        self.id = id
        self.status_estribo = "Errado"
        self.cor = getattr(Fast.ColorPrint, random.choice(
            ["YELLOW", "GREEN", "BLUE", "RED"]))

    def run(self):
        try:
            self.preMount()
            asyncio.run(self.Mount())
            while not self.terminou:
                continue
            else:
                tt = timeit.default_timer()
                while timeit.default_timer() - tt <= 0.2:
                    continue
            asyncio.run(self.posMount())
        except Fast.MyException as my:
            for item in stopReasons:
                if str(my) == str(item["description"]):
                    asyncio.run(sendWsMessage("error", item))
            print("Erro meu:", my)
            return my

    def preMount(self):
        Fast.sendGCODE(arduino, "M42 P36 S255")
        self.terminou = False
        print(f"{self.cor} ID:{self.id}--> pre Mount Start{Fast.ColorPrint.ENDC}")
        print(f"Foi requisitado a montagem de {self.qtd} peças certas.")
        print(f"{self.cor} ID:{self.id}--> pre Mount Finish{Fast.ColorPrint.ENDC}")

    async def Mount(self):
        global temPeça
        pega = True
        Filter = Hole_Filter()
        Filter.start()
        erroDetectado = False
        self.infoCode = clp.getStatus()
        print("Preparando para iniciar clico de montagem, infoCode:", self.infoCode)
        # G28()
        while self.qtd != (self.corretas if self.only else self.rodada) and not intencionalStop and self.infoCode not in stopReasons:
            self.infoCode = clp.getStatus()
            print(f"Ciclo {self.rodada} iniciou, infoCode:", self.infoCode)
            for item in stopReasons:
                if self.infoCode == item['code']:
                    print("erro no inicio do ciclo.")
                    erroDetectado = True
                    break
            if erroDetectado:
                break
            self.rodada += 1
            Fast.sendGCODE(arduino, "M42 P33 S0") #desativado-ruido

            self.status_estribo = "Errado"
            # ------------ Vai ate tombador e pega ------------ #
            try:
                if pega:
                    
                    print("~~"*10)
                    tt = timeit.default_timer()
                    while not temPeça and not erroDetectado and not intencionalStop and timeit.default_timer() - tt <= 5:
                        Fast.sendGCODE(arduino, f"\n g90 \n G0 X200 Y0 F{xMaxFed}")
                        self.infoCode = clp.getStatus()
                        print("Esperando peça, infoCode:", self.infoCode)
                        for item in stopReasons:
                            if self.infoCode == item['code']:
                                print("Erro encontrado durante a espera da peça.")
                                erroDetectado = True
                                break
                            else:
                                erroDetectado = False
                        tt = timeit.default_timer()
                        while timeit.default_timer() - tt <= 1.5:
                            pass
                    else:
                        self.infoCode = clp.getStatus()
                        for item in stopReasons:
                            if self.infoCode == item['code']:
                                print("Erro encontrado antes de pegar uma nova peça")
                                erroDetectado = True
                                break
                        print("Peça Chgeou...")
                    if temPeça and not erroDetectado:
                        PegaObjeto()
                    else:
                        print("Não a peça, e deu erro, saindo... ")
                        break
                if DebugPreciso:
                    pega = False
            except MyException as my:
                for item in stopReasons:
                    if my == item["description"]:
                        await sendWsMessage("error", item)
                print("Erro meu:", my)
                await descarte("Errado")
                break

            # ------------ Acha as coordenadas parciais do furo ------------ #
            status, parafusados = Processo_Hole(None,
                                                     mainParamters['Mask_Parameters']['hole']['areaMin'],
                                                     mainParamters['Mask_Parameters']['hole']['areaMax'],
                                                     mainParamters['Mask_Parameters']['hole']['perimeter'],
                                                     mainParamters['Filtros']['HSV']['hole']['Valores'],
                                                     ids=self.id, model=self.model, rodada=self.rodada, thread=Filter)
            

            globals()["pecaReset"] += 1
            #         # ------------ Verifica se a montagme está ok ------------ #
            if status == -1:
                self.infoCode = parafusados
                erroDetectado = True
                break
            self.infoCode = clp.getStatus()
            if self.infoCode not in stopReasons:
                if parafusados == len(selected[modelo_atual])-1:
                    Fast.sendGCODE(arduino, "M42 P34 S0")
                    
                    print("Montagem finalizada. infoCode:", self.infoCode)
                    print("Iniciando processo de validação.")
                    ValidaPos = machineParamters['configuration']['informations'][
                        'machine']['defaultPosition']['validaParafuso']

                    Fast.sendGCODE(arduino, "G90")
                    Fast.sendGCODE(arduino, "g0 A360 f50000")
                    Fast.MoveTo(arduino, ('X', ValidaPos['X']), ('Y', ValidaPos['Y']), ('F', yMaxFed))
                    Fast.sendGCODE(arduino, "M42 P33 S255") #desativado-ruido
                    validar = timeit.default_timer()
                    tt = timeit.default_timer()
                    frame = globals()[
                            'frame'+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])]
                    blur = int(cv2.Laplacian(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())
                    while blur < 18:
                        frame = globals()[
                            'frame'+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])]
                        blur = int(cv2.Laplacian(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())
                        print("Blur antes:", blur)
                        if timeit.default_timer() - tt >= 10:
                            break
                    # tt = timeit.default_timer()
                    # while timeit.default_timer() - tt < 1:
                    #     pass
                    # frame = globals()[
                    #         'frame'+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])]
                    # blur = int(cv2.Laplacian(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())
                    # print("Blur depois:", blur)
                    _, encontrados, failIndex = Process_Image_Screw(frame,
                                                                    Op.extractHSValue(
                                                                        mainParamters['Filtros']['HSV']['screw']["Valores"], 'lower'),
                                                                    Op.extractHSValue(
                                                                        mainParamters['Filtros']['HSV']['screw']["Valores"], 'upper'),
                                                                    mainParamters['Mask_Parameters']['screw']['areaMin'],
                                                                    mainParamters['Mask_Parameters']['screw']['areaMax'],
                                                                    model=str(
                                                                        self.model)
                                                                    )

                    
                    validar = timeit.default_timer()-validar
                    if  not any(x in map(int, list(selected[modelo_atual].keys())) for x in failIndex) and blur >= 16:
                        self.status_estribo = "Certo"
                        self.corretas += 1
                        #edit(f"Modelo: {modelo_atual}, id: {self.id}, rodada: {self.rodada}, encontrados: {encontrados}| Blur: {cv2.Laplacian(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()}, Status: OK\n")
                        if erroDetectado:
                            break
                    else:
                        print(f"Foram fixados apenas {encontrados} parafusos.")
                        #edit(f"Modelo: {modelo_atual}, id: {self.id}, rodada: {self.rodada}, encontrados: {encontrados}| Blur: {cv2.Laplacian(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()}, Status: FAIL\n")
                        if DebugPictures:
                            d = datetime.now()
                            cv2.imwrite(
                                f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/normal/{encontrados}.jpg", cv2.resize(frame, None, fx=0.3, fy=0.3))
                            cv2.imwrite(
                                f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/filtro/{encontrados}.jpg", cv2.resize(_, None, fx=0.3, fy=0.3))
                        self.status_estribo = "Errado"
                        self.erradas += 1
                        if erroDetectado:
                            break
                else:
                    print(f"Foram parafusados apenas {parafusados} parafusos")
                    self.status_estribo = "Errado"
                    self.erradas += 1
                    if erroDetectado:
                        break
            else:
                self.status_estribo = "Errado"
                self.erradas += 1
                print("Problema encontrado antes de validar a montagem")
                break

            print("update Operation")
            operation["operation"]["right"] = self.corretas
            operation["operation"]["placed"] = self.rodada
            operation["operation"]["wrong"] = self.erradas
            await sendWsMessage("update", operation)
            print("update Operation - Finish")
            await descarte(self.status_estribo)
            print(f"{self.cor} ID:{self.id}--> {self.rodada}{Fast.ColorPrint.ENDC}")
            #Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'], 1, Pega=True) #LLLLLL
    
        Filter.stop()
        await descarte(self.status_estribo)
        self.terminou = True

    async def posMount(self):
        Fast.sendGCODE(arduino, "M42 P36 S0")
        print(f"{self.cor} ID:{self.id}--> POS Mount Start{Fast.ColorPrint.ENDC}")
        operation["operation"]["finished"] = True
        operation["operation"]["right"] = self.corretas
        operation["operation"]["wrong"] = self.erradas
        operation["operation"]["placed"] = self.rodada
        
        operation["operation"]["stopped"] = True
        operation["operation"]["finished"] = True
        operation["operation"]["running"] = False

        await sendWsMessage("update", operation)
        print("Info Code", self.infoCode)
        if intencionalStop:
            self.infoCode = 17
        for item in stopReasons:
            if self.infoCode == item['code']:
                print(f"Erro ao tentar montar a {self.rodada}ª peça")
                await logRequest(item)
                await sendWsMessage("error", item)
        print(f"{self.cor} ID:{self.id}--> POS Mount Finish{Fast.ColorPrint.ENDC}")
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Functions                                                         #


def findHole(imgAnalyse, minArea, maxArea, c_perimeter, HSValues, fixed_Point, escala_real=4.8):
    global px2mmEcho
    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    for filter_values in HSValues:
        locals()[filter_values] = np.array(
            Op.extractHSValue(HSValues, filter_values))
    mask = Op.refineMask(Op.HSVMask(imgAnalyse, locals()
                         ['lower'], locals()['upper']))
    mask_inv = cv2.bitwise_not(mask)
    chr_k = cv2.bitwise_and(imgAnalyse, imgAnalyse, mask=mask)
    distances = []
    edge, null = Op.findContoursPlus(
        mask_inv, AreaMin_A=minArea, AreaMax_A=maxArea)
    if edge:
        for info_edge in edge:
            try:
                if 20 <= int(info_edge['dimension'][0]/2):
                    cv2.putText(chr_k, str(
                        info_edge["area"]), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5)
                    cv2.drawMarker(
                        chr_k, (info_edge['centers'][0]), (0, 255, 0), thickness=3)
                    cv2.circle(chr_k, (info_edge['centers'][0]), int(info_edge['dimension'][0]/2),
                               (36, 255, 12), 2)

                    cv2.line(chr_k, (info_edge['centers'][0]),
                             fixed_Point, (255, 0, 255), thickness=3)

                    cv2.line(chr_k, (info_edge['centers'][0]),
                             (int(info_edge['centers'][0][0]), fixed_Point[1]), (255, 0, 0), thickness=3)

                    cv2.line(chr_k, (int(
                        info_edge['centers'][0][0]), fixed_Point[1]), fixed_Point, (0, 0, 255), thickness=2)
                    px2mm = 0.02318518518518518518518518518519
                    px2mmEcho = px2mm
                    a = info_edge['centers'][0][0] - fixed_Point[0]
                    b = info_edge['centers'][0][1] - fixed_Point[1]
                    distance_to_fix = (((a)*px2mm),
                                       ((b)*px2mm))


                    cv2.putText(chr_k, "Y: "+str(a*px2mm)+"mm", (50, 200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 0, 255), 5)
                    cv2.putText(chr_k, "X: "+str(b*px2mm)+"mm", (50, 250), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 0, 0), 5)

                    distances.append(distance_to_fix)
                    distances = list(dict.fromkeys(distances))
                    distances.sort(key=sortSecond)
                    cv2.putText(chr_k, str(len(
                        distances)-1), (info_edge['centers'][0]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 50, 100), 5)
                    cv2.drawContours(
                        chr_k, [info_edge['contour']], -1, (255, 255, 255), 3)
            except KeyError:
                print("KeyError:", info_edge)
    try:
        return distances, chr_k, (info_edge['dimension'][0])
    except UnboundLocalError:
        return distances, chr_k, (0)

def setCameraFilter():
    global mainParamters, camera, machineParamters
    print("Usando valores definidos no arquivo para setar o payload inicial da camera.")
    for process in mainParamters["Filtros"]["HSV"]:
        process = mainParamters["Filtros"]["HSV"][process]
        tags = "lower", "upper"
        index = 0
        colorRange = []
        for tag in tags:
            colorItem = []
            for id, item in process["Valores"][tag].items():
                names = ["hue", "sat", "val"]
                for n in names:
                    if id[0:1] in n:
                        id = n
                        break
                camera["filters"][process["Application"]
                                  ]["hsv"][id][index] = item
                colorItem.append(item)
            colorRange.append(colorItem)
            index = 1
        camera["filters"][process["Application"]
                          ]["gradient"]["color"] = Fast.HSVF2Hex(colorRange[0])
        camera["filters"][process["Application"]
                          ]["gradient"]["color2"] = Fast.HSVF2Hex(colorRange[1])

        camera["filters"][process["Application"]]["area"][0] = mainParamters["Mask_Parameters"][process["Application"]]["areaMin"]
        camera["filters"][process["Application"]]["area"][1] = mainParamters["Mask_Parameters"][process["Application"]]["areaMax"]


def setCameraHsv(jsonPayload):
    #print("Alterando Payload da camera usando a  configuração do Front.")
    global camera
    newColors = []
    for filters in jsonPayload["filters"]:
        colorGroup = []
        filterName = filters
        filters = jsonPayload["filters"][filters]["gradient"]
        for hexColor in filters:
            hexColor = filters[hexColor]
            colorGroup.append(Fast.Hex2HSVF(hexColor, print=False))
        newColors.append(colorGroup)
        for index in range(len(colorGroup)):
            jsonPayload["filters"][filterName]["hsv"]["hue"][index] = colorGroup[index][0]
            jsonPayload["filters"][filterName]["hsv"]["sat"][index] = colorGroup[index][1]
            jsonPayload["filters"][filterName]["hsv"]["val"][index] = colorGroup[index][2]
    camera = jsonPayload


def setFilterWithCamera():
    global mainParamters, camera
    #print("Alterando valores da arquivo de configuração com base no payload da Camera")
    for _ in camera["filters"]:
     #   print("~"*20)
        # print(mainP["Filtros"]["HSV"][_]["Valores"])
        lower = {}
        upper = {}
        for __ in camera["filters"][_]["hsv"]:
            lower[f"{__[0:1]}_min"] = camera["filters"][_]["hsv"][__][0]
            upper[f"{__[0:1]}_max"] = camera["filters"][_]["hsv"][__][1]
            mainParamters["Mask_Parameters"][_]["areaMin"] = camera["filters"][_]["area"][0]
            mainParamters["Mask_Parameters"][_]["areaMax"] = camera["filters"][_]["area"][1]
        Valoroes = {"lower": lower, "upper": upper}
        for k, v in Valoroes.items():
            for k1, v1 in v.items():
                mainParamters["Filtros"]["HSV"][_]["Valores"][k][k1] = v1
      #  print(_, ":", mainParamters["Filtros"]["HSV"][_]["Valores"])


async def updateCamera(payload):
    setCameraHsv(payload)
    setFilterWithCamera()


def findCircle(circle_Mask, areaMinC, areaMaxC, perimeter_size, blur_Size=3):
    circle_info = []
    blur = cv2.medianBlur(circle_Mask, blur_Size)
    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    edges = cv2.findContours(
        opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edges = edges[0] if len(edges) == 2 else edges[1]
    ids = 0
    for c in edges:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        area = cv2.contourArea(c)
        if len(approx) >= perimeter_size and areaMinC < area < areaMaxC:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            if r >= 40 and r <= 100:
                circle_info.append({"center": (x, y), "radius": r, "id": ids})
                ids += 1
    return circle_info


def findScrew(imgAnalyse, FiltrosHSV, MainJson, processos, bh=0.3, **kwargs):

    force = kwargs.get('aba', False)
    trav = False
    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    width = int(imgAnalyse.shape[1])
    height = int(imgAnalyse.shape[0])
    offset_screw = 0.00
    edge_analyze = imgAnalyse[0:height, 0:int(width * bh)]
    chr_k = imgAnalyse
    tabs = []
    for indexes in FiltrosHSV:
        if FiltrosHSV[indexes]["Application"] in processos:
            tabs.append((
                FiltrosHSV[indexes]["Application"],
                list(FiltrosHSV[indexes]['Valores'].keys()),
                FiltrosHSV[indexes]['Valores']
            ))
    for aba, keys, value in tabs:
        if not trav:
            for key in keys:
                locals()[key] = Op.extractHSValue(value, key)
        if type(force) == int:
            trav = True
        msk = Op.refineMask(Op.HSVMask(
            edge_analyze, locals()['lower'], locals()['upper']))
        cv2.rectangle(
            msk, (0, 0), (msk.shape[1], msk.shape[0]), (0, 0, 0), thickness=20)
        chr_k = cv2.bitwise_and(edge_analyze, edge_analyze, mask=msk)
        edge, _ = Op.findContoursPlus(msk,
                                      AreaMin_A=MainJson['Mask_Parameters'][aba]['areaMin'],
                                      AreaMax_A=MainJson['Mask_Parameters'][aba]['areaMax']
                                      )
        if edge:
            for info_edge in edge:
                cv2.drawContours(
                    chr_k, [info_edge['contour']], -1, (70, 255, 20), 3)
                if aba == processos[0] and not trav:
                    point_a = tuple(info_edge['contour'][0])
                    edge_analyze = imgAnalyse[point_a[1]: height, 0:width]
                    pass
                if aba == processos[1] and not trav:
                    offset_screw = round(info_edge['dimension'][0], 4)
                    cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), thickness=3)
        else:
            return offset_screw, chr_k
    return offset_screw, chr_k


def mm2coordinate(Variacao = 0, cAtual=0, hipotenusa = 160, aberturaMinima = 149.509, simul=False):
    if not simul:
        coordenadaAtual_A = (aberturaMinima - Fast.M114(arduino)['Y'])
    else:
        coordenadaAtual_A = (aberturaMinima - cAtual)
    a = RAIZ(hipotenusa**2 - (RAIZ(hipotenusa**2-coordenadaAtual_A**2)+Variacao)**2)
    print(a, aberturaMinima-a)
    return aberturaMinima-a


def RAIZ(x):
    return x**0.5

def A2B(Variacao = 0, hipotenusa = 160, aberturaMinima = 149.509):
    coordenadaAtual_A = (aberturaMinima - Fast.M114(arduino, 'R'))
    RAIZ(hipotenusa**2 - (RAIZ(hipotenusa**2-coordenadaAtual_A**2)+Variacao)**2)


def G28(Axis="A", offset=324, speed=50000):
    Fast.sendGCODE(arduino, F"G28 {Axis}")
    Fast.MoveTo(arduino, (Axis, offset), ('F', yMaxFed))
    Fast.sendGCODE(arduino, f"G92 {Axis}0")
    Fast.sendGCODE(arduino, "G92.1")
    Fast.sendGCODE(arduino, f"M17 {Axis}")

def HomingAll():
    global FisrtPickup
    Fast.sendGCODE(arduino, "G28 YA")
    Fast.sendGCODE(arduino, "G0 A324 F50000")
    Fast.sendGCODE(arduino, f"M42 P32 S255")
    Fast.sendGCODE(arduino, "G28 XZ")
    Fast.sendGCODE(arduino, "G92 X0 Y0 Z0 A0")
    Fast.sendGCODE(arduino, "G92.1")
    Fast.sendGCODE(arduino, "M17 X Y Z A")
    Fast.sendGCODE(arduino, f"M201 X{xMaxAcceleration} Y{yMaxAcceleration}  Z{zMaxAcceleration} A{aMaxAcceleration}")
    Fast.sendGCODE(arduino, F'G0 Z{125 if modelo_atual == "0" else 135} F{zMaxFedUp}')
    FisrtPickup = True


def verificaCLP(serial):
    global wrongSequence, limitWrongSequence, temPeça, ScrewWrongSequence, limitScrewWrongSequence
    #print("WS:", wrongSequence,'&' ,'SWS:', ScrewWrongSequence)
    if (wrongSequence >= limitWrongSequence) or (ScrewWrongSequence >= limitScrewWrongSequence):
        print("Sequêcina de peças erradas:", wrongSequence)
        ScrewWrongSequence, wrongSequence = 0, 0
        return 18
    
    echo = Fast.sendGCODE(serial, 'F', echo=True)
    echo = str(echo[len(echo)-1])
    if echo == "10":
        temPeça = True
        return None

    if echo != "ok":
        if echo == "shutdown":
            try:
                for item in stopReasons:
                    if item["code"] == 19:
                        asyncio.run(Resolva(item))
                        time.sleep(2)
            except Exception as exp:
                print(exp)
            shutdown_raspberry()
            return echo
        try:
            return int(echo)
        except Exception:
            pass
    return None
    

def Parafusa(pos, voltas=2, mm=0, ZFD=100, ZFU=100, dowLess=False, reset=False, Pega=False):
    speed = int(zMaxFedDown*(ZFD/100))
    deuBoa = True
    Fast.sendGCODE(arduino, f'g91')
    Fast.sendGCODE(arduino, f'g38.3 z-{pos} F{speed}')
    Fast.MoveTo(arduino, ('Z', mm),  ('F' , speed), nonSync=True)
    t0 = timeit.default_timer()
    while (timeit.default_timer() - t0 < (((voltas*40)/400)if not Pega else ((voltas*40)/3000))):
        st = Fast.M119(arduino)["z_probe"]
        #print("Status Atual: ", st, "Time:",round(timeit.default_timer() - t0,2))
        if st == "open":
            deuBoa = True
            #edit(F"OK 0 (Z: {Fast.M114(arduino, 'R')})")
            break
    else:                                                                                       # Caso o temo estoure e o loop termine de forma natural
        #edit(F"Falha 0 (Z: {Fast.M114(arduino, 'R')})")
        if not Pega:   
            Fast.sendGCODE(arduino, f"M42 P32 S0")
            Fast.sendGCODE(arduino, 'G91')                                                      # Garate que está em posição relativa 
            Fast.MoveTo(arduino, ('Z', abs(mm)+10),  ('F' , speed), nonSync=True)                             # Sobe 20mm no eixo Z
            Fast.sendGCODE(arduino, f'M201 Z{zMaxAcceleration/4}')
            Fast.sendGCODE(arduino, f'g38.3 z-{pos} F{speed}')                                  # Desce até tocar na peça usando o probe
            Fast.MoveTo(arduino, ('Z', mm),  ('F' , speed), nonSync=True)                                    # Avança mais 'x'mm para garantir a rosca correta
            Fast.sendGCODE(arduino, f"M42 P32 S255")
            t0 = timeit.default_timer()                                                         # Inicialiança o temporizador
            while (timeit.default_timer() - t0 < (voltas*40/400)):                              # Enquanto um tempo 'x' definido com base no numero de voltas desejado não execer.
                st = Fast.M119(arduino)["z_probe"]
         #       print("Status Atual: ", st, "Time:",round(timeit.default_timer() - t0,2))       # Mostra o status do sensor
                if st  == "open":                                                               # Se o sensor 'abrir', pois deu rosca até econtrar a ponta.
                    deuBoa = True                                                               # Avisa que deuBoa
                    #edit(F"OK 1 (Z: {Fast.M114(arduino, 'R')['Z']})")
                    break                                                                       # quebra o loop
            else:                                                                               # Caso não consiga
                #edit(F"Falha 1 (Z: {Fast.M114(arduino, 'R')['Z']})")
                deuBoa = False                                                                  # Avisa que deu ruim
            Fast.sendGCODE(arduino, f"M42 P32 S255")
            Fast.sendGCODE(arduino, f'M201 Z{zMaxAcceleration}')
    if reset:
        Fast.sendGCODE(arduino, "G28 Z")
    Fast.sendGCODE(arduino, 'g90')
    return deuBoa


async def descarte(valor="Errado", Deposito={"Errado": {"X": 230, "Y": 0}}):
    global Total0, wrongSequence
    if not DebugPreciso:
        pos = machineParamters["configuration"]["informations"]["machine"]["defaultPosition"]["descarte"+valor]
        Fast.sendGCODE(arduino, f"G90")
        Fast.MoveTo(arduino, ('X', pos['X']), ('Y', pos['Y']), ('F', yMaxFed))
        Fast.sendGCODE(arduino, "M42 P31 S0")
        G28()
        try:
            cicleSeconds = round(timeit.default_timer()-Total0, 1)
            await updateProduction(cicleSeconds, valor)
        except Exception as exp:
            print(exp)
            pass
        print("updateProducion - Finish")
        if valor == "Errado" and not intencionalStop:
            if operation["operation"]["running"]:
                wrongSequence += 1
                print(
                    f"{Fast.ColorPrint.YELLOW}Errado: {wrongSequence}{Fast.ColorPrint.ENDC}")
        else:
            print(f"{Fast.ColorPrint.GREEN}Certo{Fast.ColorPrint.ENDC}")
            wrongSequence = 0


def timer(total):
    horas = floor(total / 3600)
    minutos = floor((total - (horas * 3600)) / 60)
    segundos = floor(total % 60)
    return f"{horas}:{minutos}:{segundos}"


def PegaObjeto():
    global Total0, temPeça, FisrtPickup
    pegaPos = machineParamters['configuration']['informations']['machine']['defaultPosition']['pegaTombador']
    Total0 = timeit.default_timer()
    Fast.sendGCODE(arduino, "G90")
    Fast.MoveTo(arduino, ('X', pegaPos['X']),('A', 0), ('F', xMaxFed), nonSync=True)
    if not FisrtPickup:
        Fast.MoveTo(arduino, ('Y', pegaPos['Y']),('A', 0), ('Z', -5) ,('F', zMaxFedDown))
    else:
        Fast.MoveTo(arduino, ('Y', pegaPos['Y']),('A', 0),('F', yMaxFed))
        FisrtPickup = False
    Fast.sendGCODE(arduino, "M42 P31 S255")
    Fast.sendGCODE(arduino, f"G0 Y0 Z{125 if modelo_atual == '0' else 135} F{zMaxFedUp}")
    Fast.sendGCODE(arduino, "G28 Y")
    Fast.sendGCODE(arduino, "M17 X Y Z A")
    temPeça = False

def alinhar():
    alin = machineParamters['configuration']['informations']['machine']['defaultPosition']['alinhaPeca']
    Fast.sendGCODE(arduino, 'G90')
    Fast.MoveTo(arduino, ('X', alin['X']), ('Y', alin['Y']),  ('F', yMaxFed))


def Process_Image_Screw(frames, lower, upper, AreaMin, AreaMax, name="ScrewCuts", model="1"):

    img_draw = frames.copy()
    finds = 0
    Status = []
    for Pontos in globals()[name][model]:
        pa, pb = tuple(Pontos["P0"]), (Pontos["P0"][0]+Pontos["P1"][0],
                                       Pontos["P0"][1]+Pontos["P1"][1])

        cv2.drawMarker(img_draw, pa, (255, 50, 0), thickness=10)
        cv2.drawMarker(img_draw, pb, (50, 255, 0), thickness=10)
        cv2.rectangle(img_draw, pa, pb, (255, 50, 255), 10)
        show = frames[Pontos["P0"][1]:Pontos["P0"][1] + Pontos["P1"][1],
                      Pontos["P0"][0]:Pontos["P0"][0] + Pontos["P1"][0]]

        mask = Op.refineMask(Op.HSVMask(show, lower, upper), kerenelA=(10, 10))
        Cnt_A, _ = Op.findContoursPlus(
            mask, AreaMin_A=AreaMin, AreaMax_A=AreaMax)

        show = cv2.bitwise_or(show, show, None, mask)
        if Cnt_A:
            finds += 1
            Status.append(True)
            for info in Cnt_A:
                cv2.drawContours(show, [info['contour']], -1, (0, 255, 0), thickness=10,
                                 lineType=cv2.LINE_AA)

                for pp in range(len(info['contour'])):
                    info['contour'][pp][0] += pa[0]
                    info['contour'][pp][1] += pa[1]

                cv2.drawContours(img_draw, [info['contour']], -1, (0, 255, 0), thickness=10,
                                 lineType=cv2.LINE_AA)
        else:
            Status.append(False)

        cv2.putText(show, str(len(Status)), pa, cv2.FONT_HERSHEY_DUPLEX,
                    5, (255, 255, 255), 10)

        img_draw[Pontos["P0"][1]:Pontos["P0"][1] + show.shape[0],
                 Pontos["P0"][0]:Pontos["P0"][0] + show.shape[1]] = show
    cv2.putText(img_draw, str(finds), (200, 100),
                cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 0), 10)

    return img_draw, finds, [i for i, x in enumerate(Status) if not x]


def Process_Image_Hole(frame, areaMin, areaMax, perimeter, HSValues):
    img_draw = frame.copy()
    for Pontos in HoleCuts:
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #            Corta a imagem e faz as marcações               #

        show = frame[Pontos["Origin"][1] - Pontos["P0"][1]:Pontos["Origin"][1] + Pontos["P1"][1],
                     Pontos["Origin"][0] - Pontos["P0"][0]:Pontos["Origin"][0] + Pontos["P1"][0]]
        pa, pb = (Pontos["Origin"][0] - Pontos["P0"][0], Pontos["Origin"][1] - Pontos["P0"][1]), (Pontos["Origin"][0] + Pontos["P1"][0], Pontos["Origin"][1] + Pontos["P1"][1])

        cv2.drawMarker(img_draw, pa, (255, 50, 0), thickness=10)
        cv2.drawMarker(img_draw, pb, (50, 255, 0), thickness=10)
        cv2.rectangle(img_draw, pa, pb, (255, 50, 255), 10)

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #                      Procura os furos                      #

        Resultados, R, per = findHole(show, areaMin, areaMax, perimeter, HSValues, (int(
            (pb[0]-pa[0])/2), int((pb[1]-pa[1])/2)))

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #                           X-ray                            #

        img_draw[pa[1]:pb[1],
                 pa[0]:pb[0]] = R

        cv2.drawMarker(img_draw, (Pontos["Origin"][0],
                                  Pontos["Origin"][1]),
                       (255, 0, 0),
                       thickness=5,
                       markerSize=50)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                          Exibe                             #
    return Resultados, R, per, img_draw

async def Resolva(item):
    global isSolved
    isSolved = False
    await logRequest(item)
    await sendWsMessage("error", item)

async def popupResponseSolve():
    global isSolved
    isSolved = True

def edit(command, file='movments.txt'):
    log = open(file, 'a')
    log.write(f"{command} \n")
    log.close()

def Processo_Hole(frame, areaMin, areaMax, perimeter, HSValues, ids=None, model="A", rodada=0, thread=None):
    global Analise, modelo_atual, Problema, px2mmEcho, ScrewWrongSequence, wrongSequence, limitScrewWrongSequence
    Filter = thread
    #wrongSequence = 0
    ScrewWrongSequence = 0
    first = True
    parafusadas = 0
    angle = 0
    deuBoa = True
    Pos = []
    Fast.writeJson(f'Json/Analise.json', Analise)
    path = f"Images/Process/{ids}"
    cameCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['camera0Centro']
    parafCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusadeiraCentro'].copy()
    limitScrewWrongSequence = len(selected[modelo_atual])-1
    if not os.path.exists(path) and DebugPictures:
        d = datetime.now()

        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/normal")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/filtro")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/falha")

        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/validar/{rodada}")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/validar/{rodada}/normal")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/validar/{rodada}/filtro")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/validar/{rodada}/falha")
    
    def indexs(n , especial=[2,5]):
        a = "1" if int(n) in especial else "0"
        return a
    
    breakNextLoop = False
    for lados, angle in selected[modelo_atual].items():
        if breakNextLoop:
            break
        if first:
            index = indexs(lados)
            analise = Analise[modelo_atual][str(angle)][index]
            Fast.MoveTo(arduino, ('X', analise['X']), ('Y', analise['Y']), ('A', angle), ('F', yMaxFed))
            Fast.sendGCODE(arduino, "M42 P34 S255")
            tt = timeit.default_timer()
            blur = int(cv2.Laplacian(cv2.cvtColor(globals()['frame'+str(mainParamters["Cameras"]["hole"]["Settings"]["id"])],cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())
            if modelo_atual == "1":
                limit = 3 if (int(angle) == 0 or int(angle) == 270) else 16
            else:
                limit = 10
            while blur <= limit:
                blur = int(cv2.Laplacian(cv2.cvtColor(globals()['frame'+str(mainParamters["Cameras"]["hole"]["Settings"]["id"])],cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())
                print(blur)
                if timeit.default_timer() - tt >= 5:
                    breakNextLoop = True
                    break
            first = False
        posicaoXY = Fast.M114(arduino)
        if not deuBoa:
            tt = timeit.default_timer()
            while timeit.default_timer() - tt <= 2:
                pass
        infoCode = clp.getStatus()
        for item in stopReasons:
            if infoCode == item['code']:
                return -1, infoCode
        MX, MY, frame, img_draw = Filter.getData()
        #blur = int(cv2.Laplacian(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())
        #edit(f"Blur First 1 | lado {lados} :{blur}")
        if MX and MY:
            for axis in ['X', 'Y']:
                if axis ==  'Y':
                    globals()[f"medMov{model}_{axis}_{angle}_{index}"].recebido = mm2coordinate(MY)#offCC
                else:
                    globals()[f"medMov{model}_{axis}_{angle}_{index}"].recebido = MX
                globals()[f"medMov{model}_{axis}_{angle}_{index}"].atualizaVetor()

            for axis in ['X', 'Y']:
                if globals()[f"medMov{model}_{axis}_{angle}_{index}"].atualizaMedia():
                    analise[f'offset{axis}'] = MX/10#round(globals()[f"medMov{model}_{axis}_{angle}_{index}"].media, 4)

            Pos.append(posicaoXY)

            xNOVO = -(cameCent['X']-posicaoXY['X']-MX)+parafCent['X']
            yNOVO = mm2coordinate(MY, parafCent['Y'], simul=True)  #-(cameCent['Y']-(mm2coordinate(MY*-1)))+parafCent['Y']
            posicao = {
                'X': xNOVO,   
                'Y': yNOVO,
                'A': posicaoXY['A'],
                'Z': 125 if modelo_atual == "0" else 135
            }

            Fast.MoveTo(arduino, ('X', posicao['X']), ('Y', posicao['Y']), ('Z', posicao['Z']), ('F', yMaxFed), nonSync=True)

            infoCode = clp.getStatus()
            for item in stopReasons:
                if infoCode == item['code']:
                    return -1, infoCode

            deuBoa = Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'],  parafusaCommand['mm'], zFRPD2, zFRPU2)


            if not deuBoa:
                ScrewWrongSequence += 1
                print("Seqûencia de parafusos errados:", ScrewWrongSequence)
            else:
                ScrewWrongSequence = 0
            Fast.sendGCODE(arduino, F"g0 Z{posicao['Z']+10} F {zMaxFedUp}", nonSync=True)
        temp = list(selected[modelo_atual])
        try:
            lados = temp[temp.index(lados) + 1]
            angle = selected[modelo_atual][lados]
            index = indexs(lados)
            analise = Analise[modelo_atual][str(angle)][index]
        except (ValueError, IndexError):
            break

        Fast.MoveTo(arduino, ('X', analise['X']), ('Y', analise['Y']), ('A', angle ), ('F', yMaxFed))
        
        infoCode = clp.getStatus()
        for item in stopReasons:
            if infoCode == item['code']:
                return -1, infoCode        

        if MX and MY:
            if deuBoa:
                parafusadas += 1
                if globals()["pecaReset"] >= 3:
                    Fast.sendGCODE(arduino, "G90")
                    Fast.sendGCODE(arduino, f"G0 Z-5 F{zMaxFedDown}")
                    Fast.sendGCODE(arduino, "G28 Z")
                    Fast.MoveTo(arduino, ('Z' , posicao['Z']), ('F' , zMaxFedUp), nonSync=True)
                    globals()["pecaReset"] = 0
                else:
                    Fast.sendGCODE(arduino, f"G90")
                    Fast.sendGCODE(arduino, f"G0 Z-5 F{zMaxFedDown}")
                    Fast.sendGCODE(arduino, f"G4 s0.5")
                    #Fast.sendGCODE(arduino, F"G0 Z{posicao['Z']} F{zMaxFedUp}")
                    Fast.MoveTo(arduino, ('Z' , posicao['Z']), ('F' , zMaxFedUp), nonSync=True)
                    #edit(f"Modelo: {modelo_atual}, X:{posicaoXY['X']}, Y:{posicaoXY['Y']}, A:{posicaoXY['A']} | Blur: {cv2.Laplacian(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()}, Status: OK\n")
                    #Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'], 1, Pega=True)
        else:
            #edit(f"Modelo: {modelo_atual}, X:{posicaoXY['X']}, Y:{posicaoXY['Y']}, A:{posicaoXY['A']} | Blur: {cv2.Laplacian(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()}, Status: FAIL\n")
            tt = timeit.default_timer()
            while timeit.default_timer() - tt <= 2:
                pass
            if DebugPictures:
                d = datetime.now()
                cv2.imwrite(
                    f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/falha/L{lados}_NE.jpg", cv2.resize(frame, None, fx=0.3, fy=0.3))
                cv2.imwrite(
                    f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/falha/L{lados}_FE.jpg", cv2.resize(img_draw, None, fx=0.3, fy=0.3))

    #Fast.MoveTo  arduino,  A360 F{xMaxFed}")
    #Fast.MoveTo(arduino, ('A', 360), ('F', xMaxFed), nonSync=True)
    
    return Pos, parafusadas


def sortSecond(val):
    return val[1]


def shutdown_server():
    shutdown_function = request.environ.get('werkzeug.server.shutdown')
    if shutdown_function is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_function()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                 Async-Functions                                                      #

async def updateAssembly(parm):
    global selected, assembly, machineParamters
    selected= {
        "0":{},
        "1":{}
    }
    machineParamters["configuration"]["assembly"] = assembly = parm
    convert ={"0": 0, "1":90, "2":90, "3":180, "4":270, "5":270}
    for part in parm["listOfParts"]:
        for hole in part["listOfHoles"]:
            if hole["mount"]:
                selected[str(part["index"])][str(hole["index"]-1)] = convert[str(hole["index"]-1)]
                #mm[str(hole["index"]-1)] = convert[str(hole["index"]-1)]
            print(part["index"], hole["index"], hole["mount"])
    await sendWsMessage("update", assembly)
    Fast.writeJson("Json/machineParamters.json", machineParamters)
    print(selected)


async def checkUpdate(branch="Auto_Pull"):
    subprocess.run(["git", "checkout", branch])
    subprocess.run(["git", "fetch"])
    if "Your branch is behind" in str(subprocess.check_output(["git", "status"])):
        print("Algumas alterações foram detectadas, atualizando..")
        subprocess.run(["git", "pull"])
        resp = str(subprocess.check_output(["git", "log", "-1", "--oneline"]))
        logRequest({
            "code": resp[2:9],
            "description": f"[Auto_Update]: {resp[9:len(resp)-3]}",
            "listed": False,
            "type": "info"
        })
    else:
        print("Você já está rodando a ultima versão disponivel")


async def sendParafusa(parms):
    Parafusa(parafusaCommand['Z'],
             parafusaCommand['voltas'],  parafusaCommand['mm'])


def shutdown_raspberry():
    subprocess.run(["shutdown", "now"])


async def restart_raspberry():
    subprocess.run(["reboot"])
    await asyncio.sleep(1)


async def popupTigger(parm):
    if parm != "None":
        try:
            fun = eval(parm)
            await fun()
        except NameError:
            pass


async def refreshJson():
    global maxFeedP, maxFeedrate, stopReasons, nonStopCode, xMaxFed, yMaxFed, zMaxFedDown, zMaxFedUp, eMaxFed, zFRPD2, zFRPU2, parafusaCommand, Analise, serial
    maxFeedP = machineParamters["configuration"]["informations"]["machine"]["maxFeedratePercent"]

    maxFeedrate = machineParamters["configuration"]["informations"]["machine"]["maxFeedrate"]
    stopReasons = machineParamters["configuration"]["statistics"]["stopReasons"]
    nonStopCode = machineParamters["configuration"]["statistics"]["nonStopCode"]
    parafusaCommand = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusar']

    xFRP = maxFeedP['X']
    yFRP = maxFeedP['Y']
    zFRPD = maxFeedP['ZD']
    zFRPU = maxFeedP['ZU']
    zFRPD2 = maxFeedP['ZD2']
    zFRPU2 = maxFeedP['ZU2']
    eFRP = maxFeedP['E']

    xMaxFed = int(maxFeedrate["xMax"]*(xFRP/100))
    yMaxFed = int(maxFeedrate["yMax"]*(yFRP/100))
    zMaxFedDown = int(maxFeedrate["zMaxD"]*(zFRPD/100))
    zMaxFedUp = int(maxFeedrate["zMaxU"]*(zFRPU/100))
    eMaxFed = int(maxFeedrate["aMax"]*(eFRP/100))

    allJS = {
        "allJsons": {
            "mainParamters": mainParamters,
            "machineParamters": machineParamters,
            "HoleCuts": HoleCuts,
            "ScrewCuts": ScrewCuts,
            "Analise": Analise,
            "serial": serial
        }
    }

    await sendWsMessage("update", allJS)


async def modifyJson(parms):
    for k, v in parms.items():
        globals()[k] = v
        Fast.writeJson(f'Json/{k}.json', v)
    await refreshJson()


async def updateSlider(processos):
    machineParamters['configuration']['camera']['process'] = processos
    for x in machineParamters['configuration']['camera']:
        if x[0:1] != 'p' and x[0:1] != "a":
            machineParamters['configuration']['camera'][x] = [
                mainParamters['Filtros']['HSV'][processos]['Valores']['lower'][x[0:1]+'_min'],
                mainParamters['Filtros']['HSV'][processos]['Valores']['upper'][x[0:1]+'_max']
            ]
        elif x[0:1] == "a":
            machineParamters['configuration']['camera'][x] = [
                mainParamters['Mask_Parameters'][processos]['areaMin'],
                mainParamters['Mask_Parameters'][processos]['areaMax']
            ]
        print(machineParamters['configuration']['camera'][x])


async def funcs():
    pass


async def stopProcess():
    global intencionalStop
    intencionalStop = True
    operation["operation"]["stopped"] = True
    await sendWsMessage("stopProcess_success")


async def generateError():
    item = {
        "code": random.randint(1, 100),
        "description": random.choice([
            "Houve um problema com a parte das panelas vibratórias! Por favor faça a checagem.",
            "Falta de insumo na maquina! Reponha para continuar a operação",
            "Mais de 5 peças na sequencia, foram montadas de forma errada, verifique se à algum problema."
        ]),
        "listed": random.choice([True, False]),
        "type": random.choice(["warning", "info", "error"])
    }
    await sendWsMessage("error", item)


async def stopReasonsResponse(message):
    code = message['code']
    date = message['date']
    print("Stop code:", code)
    print("Stop date:", date)
    for item in stopReasons:
        if code == item['code']:
            await logRequest(item)

    await asyncio.sleep(0.5)


async def logRequest(new_log=False):
    global logList
    if new_log:
        print("Log->", new_log)
        new_logs = {
            "code": new_log['code'],
            "description": new_log['description'],
            "type": new_log['type'],
            "date": int(round(datetime.now().timestamp()))
        }
        if new_log["listed"]:
            await stopReasonsListRequest(new_logs)
        else:
            logList["log"].append(new_logs)
    Fast.writeJson('Json/logList.json', logList)
    await sendWsMessage("update", logList)
    return


async def stopReasonsListRequest(new_request=False):
    global stopReasonsList
    if new_request:
        stopReasonsList["stopReasonsList"].append(new_request)
    Fast.writeJson('Json/stopReasonsList.json', stopReasonsList)
    await sendWsMessage("update", stopReasonsList)
    # await sendWsMessage("update", machineParamters)
    return


async def logRefresh(timeout=1):
    global logList
    date = int(round(datetime.now().timestamp()))

    M = int(datetime.fromtimestamp(date).strftime("%m"))
    Y = int(datetime.fromtimestamp(date).strftime("%Y"))
    D = int(datetime.fromtimestamp(date).strftime("%d"))

    month = datetime.fromtimestamp(date).strftime("%m")
    for log in logList['log']:
        logDate = datetime.fromtimestamp(log['date']).strftime("%m")
        if logDate != month:
            lM = int(datetime.fromtimestamp(log['date']).strftime("%m"))
            lY = int(datetime.fromtimestamp(log['date']).strftime("%Y"))
            lD = int(datetime.fromtimestamp(log['date']).strftime("%d"))
            if M-lM >= timeout and D-lD <= 0:
                logList['log'].remove(log)
            Fast.writeJson('Json/logList.json', logList)


async def startAutoCheck(date=None):
    global arduino, nano, conexaoStatusArdu, conexaoStatusNano, threadStatus, infoCode, assembly, clp
    if date and platform.system() == "Linux":
        subprocess.run(
            ["sudo", "date", "-s", f"{date[:len(date)-len('(Horário Padrão de Brasília)')]}"])
    # await updateSlider('Normal')
    await sendWsMessage("update", machineParamters)
    await sendWsMessage("update", production)
    await sendWsMessage("update", stopReasonsList)
    setCameraFilter()
    await logRefresh()
    await refreshJson()
    await updateAssembly(assembly)
    AutoCheckStatus = True
    connection = {
        "connectionStatus": "Tentantiva de conexão identificada"
    }

    await asyncio.sleep(0.1)
    await sendWsMessage("update", connection)

    connection["connectionStatus"] = "Conectando sistemas internos..."
    await sendWsMessage("update", connection)
    await asyncio.sleep(0.1)

    if not conexaoStatusArdu or not conexaoStatusNano:
        Fast.validadeUSBSerial('Json/serial.json')

    if not conexaoStatusArdu:
        connection["connectionStatus"] = "Conectando com a estação de montagem..."
        await sendWsMessage("update", connection)
        await asyncio.sleep(0.1)
        try:
            status, code, arduino = Fast.SerialConnect(
                SerialPath='Json/serial.json', name='Ramps 1.4')
            if status:
                conexaoStatusArdu = True
                HomingAll()
            else:
                raise TypeError
        except TypeError:
            connection["connectionStatus"] = "Falha ao conectar com a estação de montagem!!!"
            await sendWsMessage("update", connection)
            await asyncio.sleep(1.5)
            conexaoStatusArdu = False
            infoCode = 15

    if not conexaoStatusNano:
        connection["connectionStatus"] = "Conectando com o CLP..."
        await sendWsMessage("update", connection)
        await asyncio.sleep(0.1)
        try:
            status_nano, code_nano, nano = Fast.SerialConnect(
                SerialPath='Json/serial.json', name='Nano')
            if status_nano:
                conexaoStatusNano = True
                for _ in range (3):
                    verificaCLP(nano) #Limpa buffer de conexão.
                clp = CLP(nano, 0.1)
                clp.start()
            else:
                raise TypeError
        except TypeError:
            connection["connectionStatus"] = "Falha ao conectar com o CLP!!!"
            await sendWsMessage("update", connection)
            await asyncio.sleep(1.5)
            conexaoStatusNano = False
            infoCode = 14

    if not threadStatus:
        connection["connectionStatus"] = "Inicializando cameras..."
        await sendWsMessage("update", connection)
        await asyncio.sleep(0.1)
        try:
            globals()["thread"+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])] = CamThread(
                str(mainParamters["Cameras"]["screw"]["Settings"]["id"]), mainParamters["Cameras"]["screw"])
            #stalker1 = ViewAnother(thread1, 5)
            globals()["thread"+str(mainParamters["Cameras"]["hole"]["Settings"]["id"])] = CamThread(
                str(mainParamters["Cameras"]["hole"]["Settings"]["id"]), mainParamters["Cameras"]["hole"])
            thread0.start()
            thread2.start()
#            for x in range(10):
#                try:
#                    globals()["thread"+str(x)].start()
#                    print(f"Aguardando 'thread{str(x)}' iniciar..")
#                    print(f"'thread{str(x)}' iniciou com sucesso.. \n")
#                except (KeyError, RuntimeError):
#                    pass
            tth0 = timeit.default_timer()
            while timeit.default_timer()-tth0 <= 20:
                try:
                    if type(globals()['frame0']) == np.ndarray and type(globals()['frame2']) == np.ndarray:
                        appTh = AppThread(ip, portBack)
                        appTh.start()
                        print("Transmissão de vídeo iniciada.")
                        threadStatus = True
                        break
                except KeyError:
                    continue
            else:
                for x in range(10):
                    try:
                        globals()["thread"+str(x)].stop()
                        print(f"Aguardando 'thread{str(x)}' parar..")
                        globals()["thread"+str(x)].join(timeout=3)
                        print(f"'thread{str(x)}' parou com sucesso.. \n")
                    except (KeyError, RuntimeError):
                        pass
                clp.stop()
                appTh.stop()
        except Exception as Exp:
            connection["connectionStatus"] = "Falha ao inicializar cameras!!!"
            await sendWsMessage("update", connection)
            await asyncio.sleep(1.5)
            threadStatus = False
            print(Exp)

    if not conexaoStatusArdu or not conexaoStatusNano or not threadStatus:
        connection["connectionStatus"] = "Problemas foram encontrados..."
        await sendWsMessage("update", connection)

        for item in stopReasons:
            if infoCode == item['code']:
                print(item)
                await logRequest(item)
                await sendWsMessage("error", item)
        await asyncio.sleep(0.5)

    connection["connectionStatus"] = "Verificação concluida"
    await sendWsMessage("update", connection)
    await logRequest()
    await sendWsMessage("startAutoCheck_success")

    return AutoCheckStatus


async def startProcess(parm):
    global modelo_atual
    qtd, only, model = int(parm['total']), parm['onlyCorrectParts'], str(
        parm['partId'])
    modelo_atual = model
    #t0 = timeit.default_timer()
    NewMont = Process(qtd, Fast.randomString(
        tamanho=5, pattern=""), model=modelo_atual, only=only)
    NewMont.start()
    if DebugPictures:
        Fast.removeEmptyFolders("Images/Process")
    operation["operation"]["stopped"] = False
    operation["operation"]["finished"] = False
    operation["operation"]["running"] = True
    operation["operation"]["started"] = True
    operation["operation"]["placed"] = 0
    operation["operation"]["total"] = qtd if qtd < 999 else 0
    await sendWsMessage("update", operation)
    await sendWsMessage("startProcess_success")
    # print(
    #     f"Pedido de montagem finalizado em {int(timeit.default_timer()-t0)}s")


async def updateProduction(cicleSeconds, valor):
    global production
    prodd = production["production"]["productionPartList"][int(modelo_atual)]["production"]
    all_prodd = production["production"]["allParts"]["production"]
    print("updateProducion")
    prodd["today"]["total"] += 1
    prodd["total"]["total"] += 1
    if valor != "Errado":
        print("Valor Certo")
        prodd["today"]["rigth"] += 1
        prodd["total"]["rigth"] += 1

        if cicleSeconds < prodd["total"]["timePerCicleMin"]:
            prodd["total"]["timePerCicleMin"] = cicleSeconds
        elif cicleSeconds > prodd["total"]["timePerCicleMax"]:
            prodd["total"]["timePerCicleMax"] = cicleSeconds

        prodd["today"]["timesPerCicles"].append(
            cicleSeconds)
        print(">>> ", timer(cicleSeconds))
    elif not intencionalStop:
        print("Valor Errado")
        prodd["today"]["wrong"] += 1
        prodd["total"]["wrong"] += 1
    current_time = datetime.now()
    print(f"{current_time.day} vs {int(prodd['today']['day'])}")
    if int(prodd["today"]["day"]) != int(current_time.day):
        for x in range(2):
            prodd = production["production"]["productionPartList"][int(x)]["production"]
            print("Atualizando Dia de Hoje...")
            prodd["yesterday"] = prodd["today"]
            # Zera o dia de hoje
            prodd["today"] = {"day": int(
                current_time.day), "total": 0, "rigth": 0, "wrong": 0, "timePerCicle": 0, "timesPerCicles": [prodd["today"]["timePerCicle"]]}
            prodd["dailyAvarege"]["week_times"].append(
                prodd["yesterday"]["timePerCicle"])
            prodd["dailyAvarege"]["week_total"].append(
                prodd["yesterday"]["total"])
            prodd["dailyAvarege"]["week_rigth"].append(
                prodd["yesterday"]["rigth"])
            prodd["dailyAvarege"]["week_wrong"].append(
                prodd["yesterday"]["wrong"])
            week_time = prodd["dailyAvarege"]["week_times"]
            week_total = prodd["dailyAvarege"]["week_total"]
            week_rigth = prodd["dailyAvarege"]["week_rigth"]
            week_wrong = prodd["dailyAvarege"]["week_wrong"]
            appends = {"times": week_time, "total": week_total,
                    "rigth": week_rigth, "wrong": week_wrong}
            if week_time:
                for k, v in appends.items():
                    while len(v) > 7:
                        v.pop(0)
                    media = (np.around(np.average(np.array(v), axis=0).tolist())).tolist()#round(sum(v) / len(v), 2)
                    print(k, v, media)
                    prodd["dailyAvarege"][k] = media
        else:
            prodd = production["production"]["productionPartList"][int(modelo_atual)]["production"]
    valores = prodd["today"]["timesPerCicles"]
    if valores:
        #media = round(sum(valores) / len(valores), 2)
        media = (np.around(np.average(np.array(valores), axis=0).tolist())).tolist()
        prodd["today"]["timePerCicle"] = media
    Fast.writeJson('Json/production.json', production)

    tt = 0
    tr = 0
    tw = 0
    ttmin=0
    ttmax=0
    
    tdt = 0
    tdr = 0
    tdw = 0
    tdtc = 0

    ydt = 0
    ydr = 0
    ydw = 0
    ydtc = 0

    dat = 0
    dar = 0
    daw = 0
    datpc = 0

    dtw_ttpc = []
    tdtcs = []
    dtw_t = []
    dtw_w = []
    dtw_r = []
    tdd=[]
    ydd=[]
    ydtcs = []
    tdtcs = []
    dat = []
    dar = []
    daw = []
    datpc = []
    
    for mod in production["production"]["productionPartList"]:
        tt += mod["production"]["total"]["total"]
        tr += mod["production"]["total"]["rigth"]
        tw += mod["production"]["total"]["wrong"]
        
        ttmin += mod["production"]["total"]["timePerCicleMin"]
        ttmax += mod["production"]["total"]["timePerCicleMax"]
        
        tdd.append(mod["production"]["today"]["day"])
        tdt += mod["production"]["today"]["total"]
        tdr += mod["production"]["today"]["rigth"]
        tdw += mod["production"]["today"]["wrong"]
        
        tdtcs += mod["production"]["today"]["timesPerCicles"]
        
        ydd.append(mod["production"]["today"]["day"])
        ydt += mod["production"]["yesterday"]["total"]
        ydr += mod["production"]["yesterday"]["rigth"]
        ydw += mod["production"]["yesterday"]["wrong"]
        ydtcs += mod["production"]["yesterday"]["timesPerCicles"]

        dat.append(mod["production"]["dailyAvarege"]["total"])
        dar.append(mod["production"]["dailyAvarege"]["rigth"])
        daw.append(mod["production"]["dailyAvarege"]["wrong"])
        datpc.append(mod["production"]["dailyAvarege"]["times"])
    
        dtw_t.append(np.array(mod["production"]["dailyAvarege"]["week_total"].copy(), dtype=object))
        dtw_r.append(np.array(mod["production"]["dailyAvarege"]["week_rigth"].copy(), dtype=object))
        dtw_w.append(np.array(mod["production"]["dailyAvarege"]["week_wrong"].copy(), dtype=object))
        dtw_ttpc.append(np.array(mod["production"]["dailyAvarege"]["week_times"].copy(), dtype=object))
        
    all_prodd["dailyAvarege"]["total"] = (np.around(np.average(np.array(dat), axis=0).tolist())).tolist()
    all_prodd["dailyAvarege"]["rigth"] = (np.around(np.average(np.array(dar), axis=0).tolist())).tolist()
    all_prodd["dailyAvarege"]["wrong"] = (np.around(np.average(np.array(daw), axis=0).tolist())).tolist()
    all_prodd["dailyAvarege"]["times"] = (np.around(np.average(np.array(datpc), axis=0).tolist())).tolist()

    #print((np.around(np.average(np.array(dtw_t), axis=0).tolist())))
    all_prodd["dailyAvarege"]["week_total"] = (np.around(np.average(np.array(dtw_t), axis=0).tolist())).tolist()
    all_prodd["dailyAvarege"]["week_rigth"] = (np.around(np.average(np.array(dtw_r), axis=0).tolist())).tolist() 
    all_prodd["dailyAvarege"]["week_wrong"] = (np.around(np.average(np.array(dtw_w), axis=0).tolist())).tolist()
    all_prodd["dailyAvarege"]["week_times"] = (np.around(np.average(np.array(dtw_ttpc), axis=0).tolist())).tolist()

    all_prodd["total"]["total"] = tt
    all_prodd["total"]["rigth"] = tr
    all_prodd["total"]["wrong"] = tw

    all_prodd["today"]["total"] = tdt
    all_prodd["today"]["rigth"] = tdr
    all_prodd["today"]["wrong"] = tdw
    all_prodd["today"]["timePerCicle"] = (np.around(np.average(np.array(tdtcs), axis=0).tolist())).tolist()
    all_prodd["today"]["timesPerCicles"] = np.around(np.array(tdtcs)).tolist()

    all_prodd["yesterday"]["total"] = ydt
    all_prodd["yesterday"]["rigth"] = ydr
    all_prodd["yesterday"]["wrong"] = ydw
    all_prodd["yesterday"]["timePerCicle"] = (np.around(np.average(np.array(ydtcs), axis=0).tolist())).tolist()
    all_prodd["yesterday"]["timesPerCicles"] = np.around(np.array(ydtcs)).tolist()

    all_prodd["total"]["timePerCicleMin"] = round(ttmin/len(production["production"]["productionPartList"]), 2)
    all_prodd["total"]["timePerCicleMax"] = round(ttmax/len(production["production"]["productionPartList"]), 2)
    

    # if tdd.count(tdd[0]) == len(tdd):
    # if ydd.count(ydd[0]) == len(ydd):
        
    print("Escrevendo")
    Fast.writeJson('Json/production.json', production)
    await sendWsMessage("update", production)


async def updateMistakes(payload, id):
    global production
    mistk = production["production"]["productionPartList"][int(modelo_atual)]["mistakes"]
    for n in payload:
        mistk[f"F{n}"][f"{id}"] = False
    Fast.writeJson('Json/production.json', production)
        
async def updateMistake(payload, id):
    global production
    today = production["production"]["productionPartList"][int(modelo_atual)]["mistakes"]["today"]
    month = production["production"]["productionPartList"][int(modelo_atual)]["mistakes"]["month"]
    if len(payload["failIndex"]) > 0:
        if today["day"] != int((datetime.now()).day):
            month.append(today)
            today = {
                "day": int((datetime.now()).day),
                "data": [
                    {
                        "id": id,
                        "fail": [
                            {
                                "round": payload["round"],
                                "failIndex": payload["failIndex"]
                            }
                        ]
                    }
                ]
            }
            production["production"]["productionPartList"][int(modelo_atual)]["mistakes"]["today"] =  today
            #month.append(today)
            while len(month) > 30:
                month.pop(0)
        elif today["data"][len(today["data"])-1]["id"] == id:
            today["data"][len(today["data"])-1]["fail"].append(payload)
        else:
            today["data"].append({"id": id, "fail": [payload]})


async def saveCamera(none):
    Fast.writeJson('Json/mainParamters.json', mainParamters)
    globals()["tempFileFilter"] = mainParamters["Filtros"]["HSV"]
    print("salvei")


async def restoreCamera():
    setFilterWithCamera(mainParamters, camera, True)
    print('a')


async def sendWsMessage(command, parameter=None):
    global ws_message
    ws_message["command"] = command
    ws_message["parameter"] = parameter

    # ident deixa o objeto mostrando bonito
    cover_msg = json.dumps(ws_message, indent=2, ensure_ascii=False)
    await ws_connection.send(cover_msg)

async def updateUsers(parm):
    print(parm)
    machineParamters["configuration"]["informations"]["users"] = parm
    Fast.writeJson('Json/machineParamters.json', machineParamters)
    print(machineParamters["configuration"]["informations"]["users"])
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                       Exec                                                           #

def precisionTest(id):
    c = 0
    mm = 30
    Fast.sendGCODE(arduino, "G90")
    while True:
        for x in range(6):
            #Fast.MoveTo  arduino,  Y{mm2coordinate(mm)}")
            Fast.MoveTo(arduino, ('Y', mm2coordinate(mm)), ('F', yMaxFed))
            
            Fast.M400(arduino)
            t0 =timeit.default_timer()
            while timeit.default_timer() - t0 <=2:
                frame = globals()[
                    'frame'+str(mainParamters["Cameras"]["hole"]["Settings"]["id"])]    
            c += 1
            cv2.imwrite(f'TESTE_Image/{c}.jpg', frame)
            #Fast.MoveTo  arduino,  Y{10}")
            Fast.MoveTo(arduino, ('Y', 10), ('F', yMaxFed))
            Fast.sendGCODE(arduino, "G91")
#            Fast.MoveTo  arduino,  X{-50}")
            Fast.MoveTo(arduino, ('X', -50), ('F', xMaxFed))
            #Fast.MoveTo  arduino,  X{50}")
            Fast.MoveTo(arduino, ('X', 50), ('F', xMaxFed))
            Fast.sendGCODE(arduino, "G90")
            Fast.M400(arduino)
        Fast.sendGCODE(arduino, 'G28 Y')

if __name__ == "__main__":
    app = Flask(__name__)
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                        Load-Json                           #
    Problema = []


    #medMovY = mediaMovel(10)

    mainParamters = Fast.readJson('Json/mainParamters.json')
    serial = Fast.readJson('Json/serial.json')
    machineParamters = Fast.readJson('Json/machineParamters.json')
    logList = Fast.readJson('Json/logList.json')
    stopReasonsList = Fast.readJson('Json/stopReasonsList.json')
    HoleCuts = Fast.readJson("../engine/Json/HoleCuts.json")
    ScrewCuts = Fast.readJson("../engine/Json/ScrewCuts.json")
    Analise = Fast.readJson("Json/Analise.json")
    production = Fast.readJson("Json/production.json")
    parafusaCommand = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusar']
    camera = machineParamters["configuration"]["camera"]
    assembly = machineParamters["configuration"]["assembly"]
    globals()["tempFileFilter"] = mainParamters["Filtros"]["HSV"]
    globals()["pecaReset"] = 0
    FisrtPickup = False
    modelo_atual = "1"
    selected= {
        "0":{},
        "1":{}
    }
    temPeça = True
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                      Json-Variables                        #
    for model in ["0", "1"]:
        for axis in ['X', 'Y']:
            for angle in [0, 90, 180, 270]:
                for stage in ["0", "1"]:
                    globals()[f"medMov{model}_{axis}_{angle}_{stage}"] = mediaMovel(10, inicializador=Analise[model][str(angle)][stage][f"offset{axis}"])

    # if mainParamters["Recover"]["Status"]:
    #     mainParamters["Recover"]["Status"] = False
    #     Fast.writeJson('Json/mainParamters.json', mainParamters)
    #     print(mainParamters["Recover"]["Coords"])
    # for K, V in mainParamters["Recover"]["Coords"].items():
    #     if V == None:
    #         print("Deu ruim na hora do save, vai ser nescessário reiniciar todo o processo")
    #         break
    # else:
    #     for K, V in mainParamters["Recover"]["Coords"].items():
    #         print(f"G0 {K}{V}")

    primeiraConexao = True
    conexaoStatusArdu, conexaoStatusNano, threadStatus, infoCode = False, False, False, 0

    # sattus, code, arduino = Fast.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')
    # sattus_nano, code_nano, nano = Fast.SerialConnect(SerialPath='Json/serial.json', name='Nano')

    DebugTypes = mainParamters['Debugs']

    if DebugTypes["all"]:
        DebugPrint = DebugPictures = DebugRT = DebugMarkings = True
        DebugControls = False
    else:
        DebugPrint = DebugTypes["print"]
        DebugPictures = DebugTypes["pictures"]
        DebugRT = DebugTypes["realTime"]
        DebugMarkings = DebugTypes["markings"]
        DebugControls = DebugTypes["testControls"]
        DebugDireto = DebugTypes["direto"]
        DebugPreciso = DebugTypes["preciso"]

    maxFeedP = machineParamters["configuration"]["informations"]["machine"]["maxFeedratePercent"]

    maxFeedrate = machineParamters["configuration"]["informations"]["machine"]["maxFeedrate"]
    MaxAcceleration = machineParamters["configuration"]["informations"]["machine"]["MaxAcceleration"]
    stopReasons = machineParamters["configuration"]["statistics"]["stopReasons"]
    nonStopCode = machineParamters["configuration"]["statistics"]["nonStopCode"]

    xFRP = maxFeedP['X']
    yFRP = maxFeedP['Y']
    zFRPD = maxFeedP['ZD']
    zFRPU = maxFeedP['ZU']
    zFRPD2 = maxFeedP['ZD2']
    zFRPU2 = maxFeedP['ZU2']
    eFRP = maxFeedP['E']

    xMaxFed = int(maxFeedrate["xMax"]*(xFRP/100))
    yMaxFed = int(maxFeedrate["yMax"]*(yFRP/100))
    zMaxFedDown = int(maxFeedrate["zMaxD"]*(zFRPD/100))
    zMaxFedUp = int(maxFeedrate["zMaxU"]*(zFRPU/100))
    eMaxFed = int(maxFeedrate["aMax"]*(eFRP/100))

    xMaxAcceleration = MaxAcceleration["X"]
    yMaxAcceleration = MaxAcceleration["Y"]
    zMaxAcceleration = MaxAcceleration["Z"]
    aMaxAcceleration = MaxAcceleration["A"]
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                        Variables                           #

    StartedStream = False
    intencionalStop = False
    AP = True
    nano = "Ponteiro_Thread"
    arduino = "Ponteiro_Thread"
    clp = "Ponteiro_Thread"
    wrongSequence = 0
    ScrewWrongSequence = 0
    limitWrongSequence = 6
    limitScrewWrongSequence = 4
    portFront = machineParamters["configuration"]["informations"]["port"]
    portBack = machineParamters["configuration"]["informations"]["portStream"]
    offSetIp = 0

    if platform.system() == "Windows":
        prefix = socket.gethostbyname(socket.gethostname()).split('.')
        ip = '.'.join(['.'.join(prefix[:len(prefix) - 1]),
                       str(int(prefix[len(prefix) - 1]) + offSetIp)])
    else:
        gw = literal_eval(os.popen("ip -j route show").read())
        for _ in gw:
            if _["dev"] == "wlan0":
                gw = _
                break
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw["prefsrc"], 0))
        ip = s.getsockname()[0]
#        gateway = gw["gateway"]
        host = socket.gethostname()
        print("IP:", ip, " Host:", host)

    cameraList = []
    for filters, value in mainParamters["Cameras"].items():
        cameraList.append({
            "name": value['Settings']['title'],
            "cameraId": value['Settings']['id'],
            "filter": filters
        }
        )
    machineParamters["configuration"]["cameraList"] = cameraList
    machineParamters["configuration"]["informations"]["ip"] = ip
    Fast.writeJson('Json/machineParamters.json', machineParamters)

    functionLog = machineParamters['configuration']["statistics"]["functionsCode"]

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                      Start-Threads                         #

    globals()["thread"+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])] = CamThread(
        str(mainParamters["Cameras"]["screw"]["Settings"]["id"]), mainParamters["Cameras"]["screw"])
    #stalker1 = ViewAnother(thread1, 5)
    globals()["thread"+str(mainParamters["Cameras"]["hole"]["Settings"]["id"])] = CamThread(
        str(mainParamters["Cameras"]["hole"]["Settings"]["id"]), mainParamters["Cameras"]["hole"])
    #stalker0 = ViewAnother(thread0, 5)
    appTh = AppThread(ip, portBack)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                          Routes                            #

    @app.route('/')
    def homepage():
        return 'App vem Aqui?.'

    @app.route('/exit', methods=['GET'])
    def shutdown():
        cv2.destroyAllWindows()
        print("Pediu pra parar.")
        for x in range(10):
            try:
                globals()["thread"+str(x)].stop()
                print(f"Aguardando 'thread{str(x)}' parar..")
                globals()["thread"+str(x)].join()
                print(f"'thread{str(x)}' parou com sucesso.. \n")
            except (KeyError, RuntimeError):
                pass
        # thread0.stop()
        # thread1.stop()
        shutdown_server()
        print("Esperando Threads Serem Finalizadas")
        # appTh.join()
        loop.call_soon_threadsafe(loop.stop)  # here
        print("Aguardando 'mainThread' parar...")
        mainThread.join()
        print("Threads Finalizadas com sucesso.")
        return "Server Fechado"

    @app.route('/config', methods=['GET', 'POST'])
    def all_data():
        if request.method == 'POST':
            post_data = request.get_json()
            print(post_data)
        return jsonify({
            'status': 'success',
            'machineParamters': mainParamters
        })

    @app.route('/<valor>/<id>')
    def video_feed(valor, id):
        global LastCamID
        Esse = getattr(globals()['thread'+str(id)], "Procs")
        for processo in Esse:
            Esse[processo] = True if processo == valor else False
        print("Chamando...")
        return Response(getattr(globals()['thread'+str(id)], "ViewCam")(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                    Inside-Async-Def                        #

    async def serialMonitor(obj):
        if str(obj).upper() == "REBOOT":
            await restart_raspberry()
        elif str(obj).upper() == "G28 Z":
            Fast.sendGCODE(arduino, 'G28 Z')
            Fast.sendGCODE(arduino, 'G0 Z150 f10000')
        else:
            Fed = obj.find('F')
            if Fed != -1:
                speed = int(obj[Fed+1:len(obj)])
                for ax in ['X', 'Y', 'Z', 'A']:
                    a = ax if obj.find(ax) != -1 else -1
                    if a != -1:
                        break
                
                Newspeed = int(maxFeedrate[f"{a.lower()}Max"]*((speed/10)/100))
                obj = obj.replace(str(speed), str(Newspeed)) 
            Resposta = Fast.sendGCODE(arduino, str(obj), echo=True)
            for msg in Resposta:
                await sendWsMessage("serialMonitor_response", msg)
            print("Gcode:" + obj)
        return

    async def actions(message):
        # Verifica se afunção requisita existe e executa.
        if DebugPrint:
            print("Recebeu chamado:", message)
        command = message["command"]
        try:
            funcs = eval(command)
            try:
                await funcs(message["parameter"])
            except KeyError:
                try:
                    await funcs()
                except Fast.MyException as my:
                    await sendWsMessage(str(command)+"_success")
                    for item in stopReasons:
                        if str(my) == str(item["description"]):
                            await sendWsMessage("error", item)
        except NameError as nmr:
            print(nmr)
            print(command+"() não é uma função válida.")

    async def echo(websocket, path):
        global ws_connection
        ws_connection = websocket
        async for message in ws_connection:
            if DebugPrint:
                print(json.loads(message))
                print("~~~~~~~~~~~~~~"*20)
            await actions(json.loads(message))

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                      PreLaunch                             #

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                      Server-Start                          #

    asyncio.get_event_loop().run_until_complete(
        websockets.serve(echo, ip, portFront, ping_interval=5000, ping_timeout=5000))
    print(f"server iniciado em {ip}:{portFront}")
    try:
        loop = asyncio.get_event_loop()
        mainThread = Thread(target=loop.run_forever)
        mainThread.start()
        print('Started!')
        #ever = asyncio.get_event_loop()
        # ever.run_forever()
    except KeyboardInterrupt:
        print("Fechando conexão com webscokets na base da força")
        # ever.join()
        try:
            cv2.destroyAllWindows()
        except cv2.error:
            pass
        exit(200)
