# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
# Nota: Use Crtl + Shift + -    para colapsar todo o código e facilitar a visualização.
#
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #

"""
trasnformar infCode em uma lsita[] que se atualizata o tempo inteiro atraves de umathread.
sempre que for tratar o erro, rodar um for na lsita e seguir a trativa atual. 
o numero "10", com peça, não entra na lista, só muda a variavel assim que chegar.
"""

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
        "onlyCorrectParts": False
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
        #print("Return: X[", self.Mx,"] | Y[", self.My,"]")
        edit(f"Retornando centro do filtro > X:{self.Mx}, Y:{self.My}")
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

        # for k, v in cam_json["Properties"].items():
        #     cam.set(getattr(cv2, 'CAP_PROP_' + k), v)

        if cam.isOpened():                            # Verifica se foi aberta
            rval, frame = cam.read()                  # Lê o Status e uma imagem
            # if frame.shape[1] != cw or frame.shape[0] != ch:
            #     sendWsMessage('erro', {'codigo': "Wronge image size", 'menssagem': f'A imagem deveria ter:{cw} x {ch}, mas tem {frame.shape[1]} x {frame.shape[0]}' })
        else:
            globals()[f'frame{previewName}'] = cv2.imread(
                f"../engine_H/Images/{camID}.jpg")
            rval = False

        while rval and not self.stopped():                                   # Verifica e camera ta 'ok'

            rval, frame = cam.read()                  # Atualiza
            frame = cv2.blur(frame, (3, 3))
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
                                      [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
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
                                      [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                       + b'\r\n')
            if self.Procs['normal']:
                # print("normal")
                frame = globals()['frame'+self.previewName].copy()
                cv2.drawMarker(
                    frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)), (255, 50, 0), 0, 1000, 5)
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
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
                #tempo modificado time.sleep(0.2)
            asyncio.run(self.posMount())
        except Fast.MyException as my:
            for item in stopReasons:
                if my == item["description"]:
                    asyncio.run(sendWsMessage("error", item))
            print("Erro meu:", my)
            return my

    def preMount(self):
        Fast.sendGCODE(arduino, "M42 P36 S255")
        self.terminou = False
        print(f"{self.cor} ID:{self.id}--> pre Mount Start{Fast.ColorPrint.ENDC}")
        print(f"Foi requisitado a montagem de {self.qtd} peças certas.")

        # self.cameCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['camera0Centro']
        # self.parafCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusadeiraCentro']
        # self.parafCent['Y'] = mm2coordinate(self.parafCent['Y'], reverse=True)
        # self.intervalo = {
        #             'X':self.parafCent['X']-self.cameCent['X'],
        #             'Y':self.parafCent['Y']-self.cameCent['Y']
        #             }

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
            self.rodada += 1
            Fast.sendGCODE(arduino, "M42 P33 S0")
            Fast.sendGCODE(arduino, "M42 P34 S255") #desativado-ruido

            self.status_estribo = "Errado"
            # ------------ Vai ate tombador e pega ------------ #
            try:
                if pega:
                    
                    print("~~"*10)
                    while not temPeça and not erroDetectado:
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
            Fast.sendGCODE(arduino, "M42 P34 S0")
            Fast.sendGCODE(arduino, "M42 P33 S255") #desativado-ruido

            globals()["pecaReset"] += 1
            #         # ------------ Verifica se a montagme está ok ------------ #
            if status == -1:
                self.infoCode = parafusados
                erroDetectado = True
                break
            self.infoCode = clp.getStatus()
            if self.infoCode not in stopReasons and not intencionalStop:
                print("Parafusados :", parafusados, "vs len()-1:",len(selected[modelo_atual])-1 )
                if parafusados == len(selected[modelo_atual])-1:
                    # montar=sum(montar)
                    print("Montagem finalizada. infoCode:", self.infoCode)
                    print("Iniciando processo de validação.")
                    ValidaPos = machineParamters['configuration']['informations'][
                        'machine']['defaultPosition']['validaParafuso']

                    Fast.sendGCODE(arduino, "G90")
                    Fast.MoveTo(arduino, ('X', ValidaPos['X']), ('Y', ValidaPos['Y']), ('A', 360), ('F', yMaxFed))
                    #Fast.M400(arduino)

                    # Fast.sendGCODE(arduino, "M42 P34 S0")      #aaaaaaaax
                    # Fast.sendGCODE(arduino, "M42 P33 S255")    #aaaaaaaax

                    #Fast.sendGCODE(arduino, "G28 Y") #aqui

                    #Fast.MoveTo  arduino,  E{ValidaPos['A']}, f{eMaxFed}")
                    #Fast.M400(arduino)

                    validar = timeit.default_timer()
                    tt = timeit.default_timer()
                    while timeit.default_timer() - tt <= 1.2:
                        frame = globals()[
                            'frame'+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])]
                    #tempo modificado
                    # for n in range(10):
                        # frame = globals()[
                            # 'frame'+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])]
                        # time.sleep(0.1)
                    print("Antes")
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

                    if DebugPictures:
                        d = datetime.now()
                        cv2.imwrite(
                            f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/normal/{encontrados}.jpg", cv2.resize(frame, None, fx=0.3, fy=0.3))
                        cv2.imwrite(
                            f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/filtro/{encontrados}.jpg", cv2.resize(_, None, fx=0.3, fy=0.3))
                    if encontrados == 0:
                        _, encontrados, failIndex = Process_Image_Screw(frame,
                                                                        Op.extractHSValue(
                                                                            {'lower': {'h_min': 7, 's_min': 85, 'v_min': 92}}, 'lower'),
                                                                        Op.extractHSValue(
                                                                            {'upper': {'h_max': 57, 's_max': 230, 'v_max': 242}}, 'upper'),
                                                                        mainParamters['Mask_Parameters']['screw']['areaMin'],
                                                                        mainParamters['Mask_Parameters']['screw']['areaMax'],
                                                                        model=str(
                                                                            self.model)
                                                                        )
                        if DebugPictures:
                            d = datetime.now()
                            cv2.imwrite(
                                f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/falha/{encontrados}_N.jpg", cv2.resize(frame, None, fx=0.3, fy=0.3))
                            cv2.imwrite(
                                f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/falha/{encontrados}_F.jpg", cv2.resize(_, None, fx=0.3, fy=0.3))

                    print("Depois")
                    #await updateMistakes({"round": self.rodada, "failIndex": failIndex}, self.id)
                    #await updateMistakes(failIndex, self.rodada)
                    validar = timeit.default_timer()-validar
                    if  not any(x in map(int, list(selected[modelo_atual].keys())) for x in failIndex):
                        self.status_estribo = "Certo"
                        self.corretas += 1
                    else:
                        print(f"Foram fixados apenas {encontrados} parafusos.")
                        self.status_estribo = "Errado"
                        self.erradas += 1
                else:
                    print(f"Foram parafusados apenas {parafusados} parafusos")
                    self.status_estribo = "Errado"
                    self.erradas += 1
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
    
            Fast.sendGCODE(arduino, f"G90")
            Fast.sendGCODE(arduino, f"G0 Z-5 F{zMaxFedDown}")
            Fast.sendGCODE(arduino, f"G0 Z{125 if modelo_atual == '0' else 150} F{zMaxFedUp}")
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
    #edge = findCircle(mask, minArea, maxArea, c_perimeter)
    edge, null = Op.findContoursPlus(
        mask_inv, AreaMin_A=minArea, AreaMax_A=maxArea)
    #cv2.imshow("Mascara", cv2.resize(mask, None, fx=0.3, fy=0.3))
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
                    #print((escala_real/(info_edge['dimension'][0])))
                    #px2mm = 0.026975195072293106
                    px2mm = 0.02318518518518518518518518518519
                    #x = 0.02179487179487179487179487179487
                    px2mmEcho = px2mm
                    a = info_edge['centers'][0][0] - fixed_Point[0]
                    b = info_edge['centers'][0][1] - fixed_Point[1]
                    distance_to_fix = (((a)*px2mm),
                                       ((b)*px2mm))


                    cv2.putText(chr_k, str(a), (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 0, 0), 5)
                    cv2.putText(chr_k, str(a*px2mm), (50, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 0, 0), 5)
                    cv2.putText(chr_k, str(b), (50, 150), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 0, 255), 5)
                    cv2.putText(chr_k, str(b*px2mm), (50, 200), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 0, 255), 5)
                    # cv2.putText(chr_k, str(distance_to_fix[1]), (int(Circle['center'][0]), int(Circle['center'][1] / 2)),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    # cv2.putText(chr_k, str(distance_to_fix[0]), (int(Circle['center'][0] / 2), int(fixed_Point[1])),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    # cv2.putText(chr_k, str(Circle["id"]), (int(Circle["center"][0]), int(Circle["center"][1])),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

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


"""
def findHole(imgAnalyse, minArea, maxArea, c_perimeter, HSValues, fixed_Point, escala_real=5):
    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    for filter_values in HSValues:
        locals()[filter_values] = np.array(
            Op.extractHSValue(HSValues, filter_values))
    mask = Op.refineMask(Op.HSVMask(imgAnalyse, locals()
                         ['lower'], locals()['upper']))
    chr_k = cv2.bitwise_and(imgAnalyse, imgAnalyse, mask=mask)
    distances = []
    edge = findCircle(mask, minArea, maxArea, c_perimeter)
    #cv2.imshow("Mascara", cv2.resize(mask, None, fx=0.3, fy=0.3))
    for Circle in edge:
        cv2.circle(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])), int(Circle['radius']),
                   (36, 255, 12), 2)

        cv2.line(chr_k, (int(Circle['center'][0]), int(
            Circle['center'][1])), fixed_Point, (168, 50, 131))

        cv2.line(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])),
                 (int(Circle['center'][0]), fixed_Point[1]), (255, 0, 0))

        cv2.line(chr_k, (int(Circle['center'][0]), fixed_Point[1]),
                 fixed_Point, (0, 0, 255), thickness=2)

        distance_to_fix = (round((Circle['center'][0] - fixed_Point[0])*(escala_real/(Circle['radius']*2)), 2),
                           round((Circle['center'][1] - fixed_Point[1])*(escala_real/(Circle['radius']*2)), 2))
        cv2.putText(chr_k, str(distance_to_fix[1]), (int(Circle['center'][0]), int(Circle['center'][1] / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.putText(chr_k, str(distance_to_fix[0]), (int(Circle['center'][0] / 2), int(fixed_Point[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.putText(chr_k, str(Circle["id"]), (int(Circle["center"][0]), int(Circle["center"][1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)
        distances.append(distance_to_fix)
    try:
        return distances, chr_k, (Circle['radius']*2)
    except UnboundLocalError:
        return distances, chr_k, (0)

"""



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
    print("Alterando Payload da camera usando a  configuração do Front.")
    global camera
    newColors = []
    for filters in jsonPayload["filters"]:
        colorGroup = []
        filterName = filters
        filters = jsonPayload["filters"][filters]["gradient"]
        for hexColor in filters:
            hexColor = filters[hexColor]
            colorGroup.append(Fast.Hex2HSVF(hexColor, print=True))
        newColors.append(colorGroup)
        for index in range(len(colorGroup)):
            jsonPayload["filters"][filterName]["hsv"]["hue"][index] = colorGroup[index][0]
            jsonPayload["filters"][filterName]["hsv"]["sat"][index] = colorGroup[index][1]
            jsonPayload["filters"][filterName]["hsv"]["val"][index] = colorGroup[index][2]
    camera = jsonPayload


def setFilterWithCamera():
    global mainParamters, camera
    print("Alterando valores da arquivo de configuração com base no payload da Camera")
    for _ in camera["filters"]:
        print("~"*20)
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
        print(_, ":", mainParamters["Filtros"]["HSV"][_]["Valores"])


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


def mm2coordinate(x, c=160, aMin=148.509, reverse=False):
    if not reverse:
        r = aMin-(c**2 - ((c**2-aMin**2)**0.5+x)**2)**0.5
        edit(f"Convertendo {x} em {r} | reverse=False\n")
        return r
    else:
        r = ((c**2 - (aMin-x)**2)**0.5)-(c**2 - aMin**2)**0.5
        edit(f"Convertendo {x} em {r} | reverse=True\n")
        return r

    # return round((0.0059*(x**2)) + (0.2741*x) + (0.6205), 2)       # Antiga
    # return round((0.0051*(x**2)) + (0.302*x) + (0.5339), 2)        # 19/07 - 2/2 0->30
    # return round((-0.0231*(x**2))+(2.4001*x)+0.4472, 2)            # Reversa 19/07
    # return round(((x**2)*0.0035)+(0.3518*x)+0.1181,2)              # 20/07 - 0,2/0,2 0 -> 6,2

    # Piragoras tava certo :/
    return round(quero, 2)

def G28(Axis="A", offset=324, speed=50000):
    Fast.sendGCODE(arduino, F"G28 {Axis}")
    Fast.MoveTo(arduino, (Axis, offset), ('F', yMaxFed))
    Fast.sendGCODE(arduino, f"G92 {Axis}0")
    Fast.sendGCODE(arduino, "G92.1")
    Fast.sendGCODE(arduino, f"M17 {Axis}")

def HomingAll():

    Fast.sendGCODE(arduino, "G28 YA")
    Fast.sendGCODE(arduino, "G0 A324 F50000")
    Fast.sendGCODE(arduino, f"M42 P32 S255")
    Fast.sendGCODE(arduino, "G28 XZ")
    #Fast.G28(arduino, offset=-28)
    #Fast.sendGCODE(arduino, "G28 Z")
    Fast.sendGCODE(arduino, "G92 X0 Y0 Z0 A0")
    Fast.sendGCODE(arduino, "G92.1")
    Fast.sendGCODE(arduino, "M17 X Y Z A")
    #Parafusa(132, mm=5, voltas=20)
    #Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'], 1, Pega=True)
    Fast.sendGCODE(arduino, F'G0 Z{125 if modelo_atual == "0" else 150} F{zMaxFedUp}')


def verificaCLP(serial):
    global wrongSequence, limitWrongSequence, temPeça
    if wrongSequence >= limitWrongSequence:
        print("Sequêcina de peças erradas:", wrongSequence)
        wrongSequence = 0
        return 18

    
    #return "ok"
    echo = Fast.sendGCODE(serial, 'F', echo=True)
    echo = str(echo[len(echo)-1])
    if echo == "10":
        temPeça = True
        return None
    #print("Echo >>>", echo)
    if echo != "ok":
        try:
            return int(echo)
        except Exception:
            pass
    return None
    #if echo == "Comando não enviado, falha na conexão com a serial.":
        # return 4
    #    return "ok"
    #else:
    #    Fast.sendGCODE(arduino, "M42 P36 S0")
    # return echo
    

    # return strr
    # return random.choice(["ok","ok","ok","ok","ok","ok","ok","ok","ok","ok",1,"ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok",])


def Parafusa(pos, voltas=2, mm=0, ZFD=100, ZFU=100, dowLess=False, reset=False, Pega=False):
    speed = int(zMaxFedDown*(ZFD/100))
    deuBoa = True
    Fast.sendGCODE(arduino, f'g91')
    Fast.sendGCODE(arduino, f'g38.3 z-{pos} F{speed}')
    Fast.MoveTo(arduino, ('Z', mm),  ('F' , speed) )

    t0 = timeit.default_timer()
    while (timeit.default_timer() - t0 < (((voltas*40)/500)if not Pega else ((voltas*40)/3000))):
        st = Fast.M119(arduino)["z_probe"]
        print("Status Atual: ", st, "Time:",round(timeit.default_timer() - t0,2))
        if st == "open":
            deuBoa = True
            break
    else:                                                                                       # Caso o temo estoure e o loop termine de forma natural
        if not Pega:   
            Fast.sendGCODE(arduino, 'G91')                                                      # Garate que está em posição relativa 
            Fast.MoveTo(arduino, ('Z', abs(mm)+10),  ('F' , speed))                             # Sobe 20mm no eixo Z
            Fast.sendGCODE(arduino, f'g38.3 z-{pos} F{speed}')                                  # Desce até tocar na peça usando o probe
            Fast.MoveTo(arduino, ('Z', mm),  ('F' , speed) )                                    # Avança mais 'x'mm para garantir a rosca correta
            t0 = timeit.default_timer()                                                         # Inicialiança o temporizador
            while (timeit.default_timer() - t0 < (voltas*40/500)):                              # Enquanto um tempo 'x' definido com base no numero de voltas desejado não execer.
                st = Fast.M119(arduino)["z_probe"]
                print("Status Atual: ", st, "Time:",round(timeit.default_timer() - t0,2))       # Mostra o status do sensor
                if st  == "open":                                                               # Se o sensor 'abrir', pois deu rosca até econtrar a ponta.
                    deuBoa = True                                                               # Avisa que deuBoa
                    break                                                                       # quebra o loop
            else:                                                                               # Caso não consiga
                deuBoa = False                                                                  # Avisa que deu ruim

    if reset:
        Fast.sendGCODE(arduino, "G28 Z")
    Fast.sendGCODE(arduino, 'g90')
    # Fast.sendGCODE(arduino, f'g0 z{pos} F{int(zMaxFedUp*(ZFU/100))}')
    return deuBoa


async def descarte(valor="Errado", Deposito={"Errado": {"X": 230, "Y": 0}}):
    global Total0, wrongSequence
    if not DebugPreciso:
        pos = machineParamters["configuration"]["informations"]["machine"]["defaultPosition"]["descarte"+valor]
        Fast.sendGCODE(arduino, f"G90")
        Fast.MoveTo(arduino, ('X', pos['X']), ('Y', pos['Y']), ('F', yMaxFed))
        #Fast.M400(arduino)
        Fast.sendGCODE(arduino, "M42 P31 S0")
        #Fast.MoveTo  arduino,  A0 f{eMaxFed}")
        G28()
#    Fast.M400(arduino)
#    Fast.sendGCODE(arduino, f"G28 Y")
        try:
            cicleSeconds = round(timeit.default_timer()-Total0, 1)
            await updateProduction(cicleSeconds, valor)
        except Exception:
            pass
        print("updateProducion - Finish")
        if valor == "Errado" and not intencionalStop:
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
    global Total0, temPeça
    pegaPos = machineParamters['configuration']['informations']['machine']['defaultPosition']['pegaTombador']
    Total0 = timeit.default_timer()
    Fast.sendGCODE(arduino, "G90")
    #Fast.MoveTo  arduino,  X{pegaPos['X']} A0 F{xMaxFed}")
    Fast.MoveTo(arduino, ('X', pegaPos['X']),('A', 0), ('F', xMaxFed))
    Fast.MoveTo(arduino, ('Y', pegaPos['Y']),('A', 0), ('F', yMaxFed))
    #Fast.MoveTo  arduino,  Y{pegaPos['Y']} F{yMaxFed}")
    #Fast.M400(arduino)
    Fast.sendGCODE(arduino, "M42 P31 S255")
    Fast.sendGCODE(arduino, "G4 S0.3")
    Fast.sendGCODE(arduino, "G28 Y")
    Fast.sendGCODE(arduino, "M17 X Y Z A")
    temPeça = False

#    alinhar()

def alinhar():
    alin = machineParamters['configuration']['informations']['machine']['defaultPosition']['alinhaPeca']
    Fast.sendGCODE(arduino, 'G90')
    #Fast.MoveTo  arduino,  X{alin['X']} f{xMaxFed}")
    Fast.MoveTo(arduino, ('X', alin['X']), ('Y', alin['Y']),  ('F', yMaxFed))
    #Fast.MoveTo  arduino,  Y{alin['Y']} f{yMaxFed}")


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
    # cv2.imshow(f"Draw_Copy", cv2.resize(img_draw, None, fx=0.25, fy=0.25))
    # cv2.waitKey(1)
    return img_draw, finds, [i for i, x in enumerate(Status) if not x]


def Process_Image_Hole(frame, areaMin, areaMax, perimeter, HSValues):
    img_draw = frame.copy()
    for Pontos in HoleCuts:
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #            Corta a imagem e faz as marcações               #

        show = frame[Pontos["P0"][1]:Pontos["P0"][1] + Pontos["P1"][1],
                     Pontos["P0"][0]:Pontos["P0"][0] + Pontos["P1"][0]]
        pa, pb = tuple(Pontos["P0"]), (Pontos["P0"][0]+Pontos["P1"][0],
                                       Pontos["P0"][1]+Pontos["P1"][1])

        cv2.drawMarker(img_draw, pa, (255, 50, 0), thickness=10)
        cv2.drawMarker(img_draw, pb, (50, 255, 0), thickness=10)
        cv2.rectangle(img_draw, pa, pb, (255, 50, 255), 10)

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #                      Procura os furos                      #

        Resultados, R, per = findHole(show, areaMin, areaMax, perimeter, HSValues, (int(
            (pb[0]-pa[0])/2), int((pb[1]-pa[1])/2)))

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #                           X-ray                            #

        img_draw[Pontos["P0"][1]:Pontos["P0"][1] + show.shape[0],
                 Pontos["P0"][0]:Pontos["P0"][0] + show.shape[1]] = R

        cv2.drawMarker(img_draw, (int((pa[0]+pb[0])/2),
                                  int((pa[1]+pb[1])/2)),
                       (255, 0, 0),
                       thickness=5,
                       markerSize=50)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                          Exibe                             #
    #cv2.imshow("show", cv2.resize(show, None, fx=0.25, fy=0.25))
    # cv2.imshow("draw", cv2.resize(img_draw, None, fx=0.25, fy=0.25))
    # cv2.waitKey(1)
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
    global Analise, modelo_atual, Problema, px2mmEcho
    Filter = thread

    first = True
    parafusadas = 0
    angle = 0
    Pos = []
    Fast.writeJson(f'Json/Analise.json', Analise)
    path = f"Images/Process/{ids}"
    cameCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['camera0Centro']
    parafCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusadeiraCentro'].copy()
    #parafCent['Y'] = mm2coordinate(parafCent['Y'], reverse=True)
    # Pega a coordenada de inicio e aplica na formula, pra saber a quantos "mm" do "0" a maquina está.

    if not os.path.exists(path):
        d = datetime.now()

        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/normal")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/filtro")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/falha")

        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/validar/{rodada}")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/validar/{rodada}/normal")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/validar/{rodada}/filtro")
        os.makedirs(f"{path}_{str(d.day)+str(d.month)}/validar/{rodada}/falha")
    #for lados in range(6):
    def indexs(n , especial=[2,5]):
        a = "1" if int(n) in especial else "0"
        return a
        
    for lados, angle in selected[modelo_atual].items():
        if first:
            index = indexs(lados)
            analise = Analise[modelo_atual][str(angle)][index]
            # zzzzz print("Atual", lados, angle, index)
            # zzzzz print("Normal:", analise["X"], analise["Y"], '\n')
            #Fast.MoveTo  arduino,  X{analise['X']+analise['offsetX']} Y{analise['Y']+analise['offsetY']} A{angle} F{yMaxFed}")
            edit(f"Analisando lado {lados}> X:{analise['X']} Y:{analise['Y']} A:{angle} F:{yMaxFed}\n")
            Fast.MoveTo(arduino, ('X', analise['X']), ('Y', analise['Y']), ('A', angle), ('F', yMaxFed))
            #Fast.MoveTo(arduino, ('X', analise['X']+analise['offsetX']), ('Y', analise['Y']+analise['offsetY']), ('A', angle), ('F', yMaxFed))
            #Fast.M400(arduino)
            MX, MY, nada, nada2 = Filter.getData()
            edit(f"Offset encontrado X:{MX} Y:{MY} \n")
            if not MX or not MY:
                tt = timeit.default_timer()
                while timeit.default_timer()-tt <= 2:
                    pass
            first = False
            MX, MY = None, None
        # else:
        #     Fast.M400(arduino)

        posicao = Fast.M114(arduino)
        edit(f"Posicao atual da maquina > X:{posicao['X']} Y:{posicao['Y']} A:{posicao['A']} \n")
        infoCode = clp.getStatus()
        for item in stopReasons:
            if infoCode == item['code']:
                return -1, infoCode
        MX, MY, frame, img_draw = Filter.getData()
        edit(f"Offset encontrado X:{MX} Y:{MY} \n")
        if MX and MY:
            for axis in ['X', 'Y']:
                if axis ==  'Y':
                    CordenadaCC = posicao['Y']
                    offMM = MY
                    CordenadaMM = mm2coordinate(CordenadaCC)
                    CordenadaMM += offMM
                    CordenadaMMcc = mm2coordinate(CordenadaMM, reverse=True)
                    offCC = CordenadaMMcc-CordenadaCC 
                    globals()[f"medMov{model}_{axis}_{angle}_{index}"].recebido = round(offCC,4)
                else:
                    globals()[f"medMov{model}_{axis}_{angle}_{index}"].recebido = round((MX/2), 4)
                globals()[f"medMov{model}_{axis}_{angle}_{index}"].atualizaVetor()

            for axis in ['X', 'Y']:
                # zzzzz print(f"medMov{model}_{axis}_{angle}_{index}>>")
                if globals()[f"medMov{model}_{axis}_{angle}_{index}"].atualizaMedia():
                    # zzzzz print(globals()[f"medMov{model}_{axis}_{angle}_{index}"].valores)
                    # zzzzz print(globals()[f"medMov{model}_{axis}_{angle}_{index}"].media)
                    analise[f'offset{axis}'] = round(globals()[f"medMov{model}_{axis}_{angle}_{index}"].media, 4)

            Pos.append(posicao)
            """
            posYmm = mm2coordinate(posicao['Y'], reverse=True)
            posXmm = MX

            invDiffY = MY
            invDiffX = MX*-1

            posParafYmm = mm2coordinate(parafCent['Y'], reverse=True)
            posParafXmm = parafCent['X']

            poscameCentYmm = mm2coordinate(cameCent['Y'], reverse=True)
            poscameCentXmm = cameCent['X']
             
            yNOVO = round(mm2coordinate(posYmm + invDiffY + (posParafYmm - poscameCentYmm)), 3)
            xNOVO = round(posXmm + invDiffX + (posParafXmm - poscameCentXmm), 3)
            """
            offsetYFixo = 0 #0.9
            offsetXFixo = 0 #4.5

            #xNOVO = analise['X']+analise['offsetX']+MX+offsetXFixo
            xNOVO = -(cameCent['X']-posicao['X']-MX)+parafCent['X']+offsetXFixo
            yNOVO = mm2coordinate(mm2coordinate(parafCent['Y'], reverse=True)+MY+offsetYFixo)
            edit(f"Posicao de parafusar: X = -({cameCent['X']}-{posicao['X']}-{MX})+{parafCent['X']}+{offsetXFixo} >> {xNOVO} \n")
            edit(f"Posicao de parafusar: Y = mm2coordinate(mm2coordinate({parafCent['Y']}, reverse=True)+{MY}+{offsetYFixo}) >> {yNOVO} \n")
            posicao = {
                'X': xNOVO,   
                'Y': yNOVO,
                'A': posicao['A'],
                'Z': 125 if modelo_atual == "0" else 150
            }

            #Fast.MoveTo  arduino,  Y{posicao['Y']} X{posicao['X']} F{yMaxFed}")
            Fast.MoveTo(arduino, ('X', posicao['X']), ('Y', posicao['Y']), ('Z', posicao['Z']), ('F', yMaxFed))
            deuBoa = Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'],  parafusaCommand['mm'], zFRPD2, zFRPU2)
            # Fast.MoveTo(arduino, ('Z', posicao['Z']), ('F', zMaxFedUp))
            Fast.sendGCODE(arduino, F"g0 Z{posicao['Z']+10} F {zMaxFedUp}")
        temp = list(selected[modelo_atual])
        try:
            lados = temp[temp.index(lados) + 1]
            angle = selected[modelo_atual][lados]
            index = indexs(lados)
            analise = Analise[modelo_atual][str(angle)][index]
        except (ValueError, IndexError):
            break

        #Fast.MoveTo  arduino,  X{round(analise['X']+analise['offsetX'], 4)} Y{round(analise['Y']+analise['offsetY'], 4)} A{angl    e} F{yMaxFed}")
        #Fast.MoveTo(arduino, ('X', round(analise['X']+analise['offsetX'], 4)), ('Y',round(analise['Y']+analise['offsetY'], 4)), ('A', angle ), ('F', yMaxFed))
        edit(f"Analisando lado {lados}> X:{analise['X']} Y:{analise['Y']} A:{angle} F:{yMaxFed}\n")
        Fast.MoveTo(arduino, ('X', analise['X']), ('Y', analise['Y']), ('A', angle ), ('F', yMaxFed))
        

        if MX and MY:
            if deuBoa:
                edit(f"deuBoa \n")
                parafusadas += 1
                if globals()["pecaReset"] >= 3:
                    Fast.sendGCODE(arduino, "G90")
                    Fast.sendGCODE(arduino, f"G0 Z-5 F{zMaxFedDown}")
                    Fast.sendGCODE(arduino, "G28 Z")
                    #Fast.sendGCODE(arduino, F"G0 Z{posicao['Z']} F{zMaxFedUp}")
                    Fast.MoveTo(arduino, ('Z' , posicao['Z']), ('F' , zMaxFedUp))
                    #Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'], 1, reset=True, Pega=True)
                    globals()["pecaReset"] = 0
                else:
                    Fast.sendGCODE(arduino, f"G90")
                    Fast.sendGCODE(arduino, f"G0 Z-5 F{zMaxFedDown}")
                    #Fast.sendGCODE(arduino, F"G0 Z{posicao['Z']} F{zMaxFedUp}")
                    Fast.MoveTo(arduino, ('Z' , posicao['Z']), ('F' , zMaxFedUp))
                    #Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'], 1, Pega=True)
        else:
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
    Fast.MoveTo(arduino, ('A', 360), ('F', xMaxFed))
    
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


async def shutdown_raspberry():
    subprocess.run(["reboot"])
    await asyncio.sleep(1)


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
            ["date", "-s", f"{date[:len(date)-len('(Horário Padrão de Brasília)')]}"])
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
    t0 = timeit.default_timer()
    NewMont = Process(qtd, Fast.randomString(
        tamanho=5, pattern=""), model=modelo_atual, only=only)
    NewMont.start()
    Fast.removeEmptyFolders("Images/Process")
    operation["operation"]["stopped"] = False
    operation["operation"]["finished"] = False
    operation["operation"]["running"] = True
    operation["operation"]["started"] = True
    operation["operation"]["placed"] = 0
    operation["operation"]["total"] = qtd if qtd < 999 else 0
    await sendWsMessage("update", operation)
    await sendWsMessage("startProcess_success")
    print(
        f"Pedido de montagem finalizado em {int(timeit.default_timer()-t0)}s")


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
        print("Atualizando Dia de Hoje...")
        prodd["yesterday"] = prodd["today"]
        # Zera o dia de hoje
        prodd["today"] = {"day": int(
            current_time.day), "total": 0, "rigth": 0, "wrong": 0, "timePerCicle": 0, "timesPerCicles": []}
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
                media = round(sum(v) / len(v), 1)
                print(k, v, media)
                prodd["dailyAvarege"][k] = media

    valores = prodd["today"]["timesPerCicles"]
    if valores:
        media = round(sum(valores) / len(valores), 1)
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
    dtw_t = []
    dtw_w = []
    dtw_r = []
    tdd=[]
    ydd=[]
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

        tdtc += mod["production"]["today"]["timePerCicle"]

        ydd.append(mod["production"]["today"]["day"])
        ydt += mod["production"]["yesterday"]["total"]
        ydr += mod["production"]["yesterday"]["rigth"]
        ydw += mod["production"]["yesterday"]["wrong"]

        ydtc += mod["production"]["yesterday"]["timePerCicle"]

        dat += mod["production"]["dailyAvarege"]["total"]
        dar += mod["production"]["dailyAvarege"]["rigth"]
        daw += mod["production"]["dailyAvarege"]["wrong"]
        datpc += mod["production"]["dailyAvarege"]["times"]

        dtw_t.append(np.array(mod["production"]["dailyAvarege"]["week_total"], dtype=object))
        dtw_r.append(np.array(mod["production"]["dailyAvarege"]["week_rigth"], dtype=object))
        dtw_w.append(np.array(mod["production"]["dailyAvarege"]["week_wrong"], dtype=object))
        dtw_ttpc.append(np.array(mod["production"]["dailyAvarege"]["week_times"], dtype=object))
    
    all_prodd["dailyAvarege"]["total"] = dat
    all_prodd["dailyAvarege"]["rigth"] = dar
    all_prodd["dailyAvarege"]["wrong"] = daw
    all_prodd["dailyAvarege"]["times"] = datpc

    all_prodd["dailyAvarege"]["week_total"] = (np.sum(np.array(dtw_t), axis=0)).tolist() 
    all_prodd["dailyAvarege"]["week_rigth"] = (np.sum(np.array(dtw_r), axis=0)).tolist() 
    all_prodd["dailyAvarege"]["week_wrong"] = (np.sum(np.array(dtw_w), axis=0)).tolist() 
    all_prodd["dailyAvarege"]["week_times"] = (np.average(np.array(dtw_ttpc), axis=0)).tolist() 
    
    

    all_prodd["total"]["total"] = tt
    all_prodd["total"]["rigth"] = tr
    all_prodd["total"]["wrong"] = tw


    all_prodd["today"]["total"] = tdt
    all_prodd["today"]["rigth"] = tdr
    all_prodd["today"]["wrong"] = tdw
    all_prodd["today"]["timePerCicle"] = tdtc/len(tdd)

    all_prodd["yesterday"]["total"] = ydt
    all_prodd["yesterday"]["rigth"] = ydr
    all_prodd["yesterday"]["wrong"] = ydw
    all_prodd["yesterday"]["timePerCicle"] = ydtc/len(ydd)


    all_prodd["total"]["timePerCicleMin"] = ttmin/len(production["production"]["productionPartList"])
    all_prodd["total"]["timePerCicleMax"] = ttmax/len(production["production"]["productionPartList"])

    

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
    HoleCuts = Fast.readJson("../engine_H/Json/HoleCuts.json")
    ScrewCuts = Fast.readJson("../engine_H/Json/ScrewCuts.json")
    Analise = Fast.readJson("Json/Analise.json")
    production = Fast.readJson("Json/production.json")
    parafusaCommand = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusar']
    camera = machineParamters["configuration"]["camera"]
    assembly = machineParamters["configuration"]["assembly"]
    globals()["tempFileFilter"] = mainParamters["Filtros"]["HSV"]
    globals()["pecaReset"] = 0
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
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                        Variables                           #

    StartedStream = False
    intencionalStop = False
    AP = True
    nano = "Ponteiro_Thread"
    arduino = "Ponteiro_Thread"
    clp = "Ponteiro_Thread"
    wrongSequence = 0
    limitWrongSequence = 3
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
                        if my == item["description"]:
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
