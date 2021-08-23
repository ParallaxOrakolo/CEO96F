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
	"finished":False
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
        item["description"] = item["description"].replace("_id_", str(self.camID['Settings']['id']))
        await sendWsMessage("error", item)

    def camPreview(self, previewName, cam_json):
        # Abre a camera com o id passado.
        camID = cam_json["Settings"]["id"]
        cw = cam_json["Settings"]["frame_width"]
        ch = cam_json["Settings"]["frame_height"]
        print(cw,'x', ch)
        cam = cv2.VideoCapture(camID)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, int(cw))
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, int(ch))
        cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
        
        # for k, v in cam_json["Properties"].items():
        #     cam.set(getattr(cv2, 'CAP_PROP_' + k), v)

        if cam.isOpened():                            # Verifica se foi aberta
            rval, frame = cam.read()                  # Lê o Status e uma imagem
            # if frame.shape[1] != cw or frame.shape[0] != ch:
            #     sendWsMessage('erro', {'codigo': "Wronge image size", 'menssagem': f'A imagem deveria ter:{cw} x {ch}, mas tem {frame.shape[1]} x {frame.shape[0]}' })
        else:
            globals()[f'frame{previewName}'] = cv2.imread(f"../engine_H/Images/{camID}.jpg")
            rval = False

        while rval and not self.stopped():                                   # Verifica e camera ta 'ok'

            rval, frame = cam.read()                  # Atualiza
            frame = cv2.blur(frame, (3,3))
            globals()[f'frame{previewName}'] = frame
            if cv2.waitKey(1) == 27:
                break
        try:    
            cv2.destroyWindow(previewName)
        except cv2.error:
            pass
        cam.release()
        print("Saindo da thread", self.previewName)
        infoCode = 6
        for item in stopReasons:
            if infoCode == item['code']:
                asyncio.run(self.report(item))
        return False


    def ViewCam(self):
        while not self.stopped():
            if self.Procs['screw']:
                
                frame, _ = Process_Imagew_Scew(
                                    globals()['frame'+self.previewName],
                                    Op.extractHSValue(mainParamters['Filtros']['HSV']['screw']["Valores"], 'lower' ),
                                    Op.extractHSValue(mainParamters['Filtros']['HSV']['screw']["Valores"], 'upper' ),
                                    mainParamters['Mask_Parameters']['screw']['areaMin'],
                                    mainParamters['Mask_Parameters']['screw']['areaMax']
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
                cv2.drawMarker(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)),(255,50,0),0,1000, 5)
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

class Process(threading.Thread):
    def __init__(self, quantidad, id, model):
        threading.Thread.__init__(self)
        global intencionalStop, arduino, nano
        self.qtd = quantidad
        self.corretas = 0
        self.erradas = 0
        self.rodada = 0
        self.infoCode = infoCode
        intencionalStop = False # Destrava a maquina quando um novo processo é iniciado.
        self.arduino = arduino
        self.nano = nano
        self.model = model
        self.id = id
        self.cor = getattr(Fast.ColorPrint, random.choice(["YELLOW", "GREEN", "BLUE", "RED"]))

    def run(self):
        try:
            self.preMount()
            self.Mount()
            self.posMount()
        except Fast.MyException as my:
            for item in stopReasons:
                if my == item["description"]:
                    asyncio.run(sendWsMessage("error", item))
            print("Erro meu:", my)
            return my
    def preMount(self):

        print(f"{self.cor} ID:{self.id}--> pre Mount Start{Fast.ColorPrint.ENDC}")
        print(f"Foi requisitado a montagem de {self.qtd} peças certas.")

        
        # self.cameCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['camera0Centro']
        # self.parafCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusadeiraCentro']
        # self.parafCent['Y'] = NLinearRegression(self.parafCent['Y'], reverse=True)
        # self.intervalo = {
        #             'X':self.parafCent['X']-self.cameCent['X'],
        #             'Y':self.parafCent['Y']-self.cameCent['Y']
        #             }

        print(f"{self.cor} ID:{self.id}--> pre Mount Finish{Fast.ColorPrint.ENDC}")

    def Mount(self):
        Fast.sendGCODE(arduino, "M42 P36 S255")
        self.infoCode = verificaCLP(nano)
        while self.qtd != self.corretas and not intencionalStop:
            self.rodada += 1
            self.status_estribo = "Errado"
            # ------------ Vai ate tombador e pega ------------ #
            try:
                PegaObjeto()
            except MyException as Mye:
                print(Mye)
                descarte("Errado")
                break

            # ------------ Acha as coordenadas parciais do furo ------------ #
            parcialFuro, parafusados = Processo_Hole(None,
                        mainParamters['Mask_Parameters']['hole']['areaMin'],
                        mainParamters['Mask_Parameters']['hole']['areaMax'],
                        mainParamters['Mask_Parameters']['hole']['perimeter'],
                        mainParamters['Filtros']['HSV']['hole']['Valores'],
                        ids=self.id, model=self.model, rodada=self.rodada)

            globals()["pecaReset"] += 1
            # ------------ Verifica e inicia processo de parafusar  ------------ #
            # self.infoCode = verificaCLP(nano)
            # if self.infoCode in nonStopCode and not intencionalStop:
            #     if len(parcialFuro) >= 5: # Verificar qual o número certo .....
            #         montar = []
            #         tM0 = timeit.default_timer()
            #         finalFuro = []
            #         for posicao in parcialFuro:
            #             print("Posicao: ", posicao)
            #             print(-round(self.cameCent['X']-posicao['X'], 2), self.intervalo['X'])

            #             # ------------ Acha a posição final dos furos  ------------ #
            #             finalFuro.append({
            #                         'X':-round(self.cameCent['X']-posicao['X'], 2)+self.parafCent ['X'],
            #                         'Y':-round(self.cameCent['Y']-posicao['Y'], 2)+self.parafCent['Y'],
            #                         'E':posicao['E']} )

            #         # ------------ Roda a sequência de parafusar ------------ #
            #         Fast.sendGCODE(arduino, 'g90')
            #         for posicao in finalFuro:
            #             self.infoCode = verificaCLP(nano)
            #             if self.infoCode in nonStopCode and not intencionalStop:
            #                 Fast.sendGCODE(arduino, f"g0 X{posicao['X']} E{posicao['E']} F{xMaxFed}")
            #                 Fast.sendGCODE(arduino, f"g0 Y{posicao['Y']} F{yMaxFed}")
            #                 Parafusa(160, mm=2, voltas=20)
            #                 Fast.sendGCODE(arduino, f"g0 Y{1} F{yMaxFed}")
            #                 Parafusa(160, mm=5, voltas=20)
            #                 montar.append(timeit.default_timer()-tM0)
            #             else:
            #                 print("Prolema encontado durante o processo de parafusar")
            #                 break
                    
            #         # ------------ Verifica se a montagme está ok ------------ #
            if self.infoCode in nonStopCode and not intencionalStop:
                if parafusados == 6:
                    #montar=sum(montar)
                    print("Montagem finalizada.")
                    print("Iniciando processo de validação.")
                    Fast.sendGCODE(arduino, "G90")
                    ValidaPos = machineParamters['configuration']['informations']['machine']['defaultPosition']['validaParafuso']

                    Fast.sendGCODE(arduino, f"G0 Y{ValidaPos['Y']} f{yMaxFed}")
                    Fast.sendGCODE(arduino, f"G0 X{ValidaPos['X']}, f{xMaxFed}")

                    Fast.M400(arduino)

                    Fast.sendGCODE(arduino, "M42 P34 S0")
                    Fast.sendGCODE(arduino, "M42 P33 S255")
                    
                    Fast.sendGCODE(arduino, "G28 Y")
                    
                    

                    #Fast.sendGCODE(arduino, f"G0 E{ValidaPos['E']}, f{eMaxFed}")
                    Fast.M400(arduino)
                    
                    validar = timeit.default_timer()
                    for n in range(10):
                        frame = globals()['frame'+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])]
                        time.sleep(0.1)
                    print("Antes")
                    _, encontrados = Process_Imagew_Scew(frame,
                                        Op.extractHSValue(mainParamters['Filtros']['HSV']['screw']["Valores"], 'lower' ),
                                        Op.extractHSValue(mainParamters['Filtros']['HSV']['screw']["Valores"], 'upper' ),
                                        mainParamters['Mask_Parameters']['screw']['areaMin'],
                                        mainParamters['Mask_Parameters']['screw']['areaMax'],
                                        model = str(self.model)
                                        )

                    if DebugPictures:
                        d = datetime.now()
                        cv2.imwrite(f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/normal/{encontrados}.jpg", frame)
                        cv2.imwrite(f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/filtro/{encontrados}.jpg", _)
                    if encontrados == 0:
                        _, encontrados = Process_Imagew_Scew(frame,
                                            Op.extractHSValue({'lower': {'h_min': 7, 's_min': 85, 'v_min': 92}}, 'lower' ),
                                            Op.extractHSValue({'upper': {'h_max': 57, 's_max': 230, 'v_max': 242}}, 'upper' ),
                                            mainParamters['Mask_Parameters']['screw']['areaMin'],
                                            mainParamters['Mask_Parameters']['screw']['areaMax'],
                                            model = str(self.model)
                                         )
                        if DebugPictures:
                            d = datetime.now()
                            cv2.imwrite(f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/falha/{encontrados}_N.jpg", frame)
                            cv2.imwrite(f"Images/Process/{self.id}_{str(d.day)+str(d.month)}/validar/{self.rodada}/falha/{encontrados}_F.jpg", _)
                            
                    print("Depois")
#                    if DebugPictures:
#                        cv2.imshow("Validador", cv2.resize(_, None, fx=0.3, fy=0.3))
#                        cv2.waitKey(1)
                    validar = timeit.default_timer()-validar
                    if encontrados == 6:
                        self.status_estribo = "Certo"
                        self.corretas+=1
                        operation["operation"]["placed"] = self.corretas
                    else:
                        print(f"Foram fixados apenas {encontrados} parafusos.")
                        self.status_estribo = "Errado"
                        self.erradas+=1
                else:
                    print(f"Foram parafusados apenas {parafusados} parafusos")
                    self.status_estribo = "Errado"
            else:
                self.status_estribo = "Errado"
                print("Problema encontrado antes de validar a montagem")
                break
            print("update Operation")
            asyncio.run(sendWsMessage("update", operation))
            print("update Operation - Finish")
            descarte(self.status_estribo)

        #     else:
        #         print("Problema encontrado depois do processo de Scan ")
        #         print(f"Foram econtrados apenas {len(parcialFuro)} furos.")
        #         descarte("Errado")
        #         self.erradas+=1
        # else:
        #     print("Prolema encontado antes de iniciar o processo de Scan")
        #     descarte("Errado")
        #     break 

            print(f"{self.cor} ID:{self.id}--> {self.rodada}{Fast.ColorPrint.ENDC}")

    def posMount(self):
        print(f"{self.cor} ID:{self.id}--> POS Mount Start{Fast.ColorPrint.ENDC}")
        operation["operation"]["finished"] = True
        asyncio.run(sendWsMessage("update", operation))
        if intencionalStop:
            self.infoCode = 7
        for item in stopReasons:
            if self.infoCode == item['code']:
                descarte("Errado")
                print(f"Erro ao tentar montar a {self.rodada}ª peça")
                print(item)
                asyncio.run(sendWsMessage("error", item))
        print(f"{self.cor} ID:{self.id}--> POS Mount Finish{Fast.ColorPrint.ENDC}")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Functions                                                         #

def findHole(imgAnalyse, minArea, maxArea, c_perimeter, HSValues, fixed_Point, escala_real=4.4):
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
                    cv2.putText(chr_k, str(info_edge["area"]), (0,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5)
                    cv2.drawMarker(chr_k,(info_edge['centers'][0]), (0,255,0), thickness=3)
                    cv2.circle(chr_k, (info_edge['centers'][0]), int(info_edge['dimension'][0]/2),
                    (36, 255, 12), 2)
                    
                    cv2.line(chr_k, (info_edge['centers'][0]), fixed_Point, (255, 0, 255), thickness=3)

                    cv2.line(chr_k, (info_edge['centers'][0]),
                            (int(info_edge['centers'][0][0]), fixed_Point[1]), (255, 0, 0), thickness=3)

                    cv2.line(chr_k, (int(info_edge['centers'][0][0]), fixed_Point[1]), fixed_Point, (0, 0, 255), thickness=2)
                    distance_to_fix = (round(((info_edge['centers'][0][0] - fixed_Point[0])*(escala_real/(info_edge['dimension'][0]))), 2),
                                    round(((info_edge['centers'][0][1] - fixed_Point[1])*(escala_real/(info_edge['dimension'][0]))), 2))

                    # cv2.putText(chr_k, str(distance_to_fix[1]), (int(Circle['center'][0]), int(Circle['center'][1] / 2)),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    # cv2.putText(chr_k, str(distance_to_fix[0]), (int(Circle['center'][0] / 2), int(fixed_Point[1])),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    # cv2.putText(chr_k, str(Circle["id"]), (int(Circle["center"][0]), int(Circle["center"][1])),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

                    distances.append(distance_to_fix)
                    distances = list(dict.fromkeys(distances))
                    distances.sort(key = sortSecond)
                    cv2.putText(chr_k, str(len(distances)-1), (info_edge['centers'][0]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (255, 50, 100), 5)
                    cv2.drawContours(chr_k, [info_edge['contour']], -1, (255, 255, 255), 3)
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
                camera["filters"][process["Application"]]["hsv"][id][index] = item
                colorItem.append(item)
            colorRange.append(colorItem)
            index = 1
        camera["filters"][process["Application"]]["gradient"]["color"] = Fast.HSVF2Hex(colorRange[0])
        camera["filters"][process["Application"]]["gradient"]["color2"] = Fast.HSVF2Hex(colorRange[1])


def setCameraHsv(jsonPayload):
    print("Alterando Payload da camera usando a  configuração do Front.")
    global camera
    newColors = []
    for filters in jsonPayload["filters"]:
        colorGroup= []
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
        #print(mainP["Filtros"]["HSV"][_]["Valores"])
        lower = {}
        upper = {}
        for __ in camera["filters"][_]["hsv"]:
            lower[f"{__[0:1]}_min"] = camera["filters"][_]["hsv"][__][0]
            upper[f"{__[0:1]}_max"] = camera["filters"][_]["hsv"][__][1]
        Valoroes = {"lower":lower, "upper":upper}
        for k, v  in Valoroes.items():
            for k1, v1  in v.items():
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
            if r >= 40 and r<=100:
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
                    offset_screw = round(info_edge['dimension'][0], 3)
                    cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), thickness=3)
        else:
            return offset_screw, chr_k
    return offset_screw, chr_k

   
def NLinearRegression(x, c=160, aMin=152.61, reverse=False):
    if not reverse:
        return round(aMin-(c**2 - ((c**2-aMin**2)**0.5+x)**2)**0.5, 2)
    else:
        return round(((c**2 - (aMin-x )**2)**0.5)-(c**2- aMin**2)**0.5, 2)

    #return round((0.0059*(x**2)) + (0.2741*x) + (0.6205), 2)       # Antiga
    #return round((0.0051*(x**2)) + (0.302*x) + (0.5339), 2)        # 19/07 - 2/2 0->30
    #return round((-0.0231*(x**2))+(2.4001*x)+0.4472, 2)            # Reversa 19/07
    #return round(((x**2)*0.0035)+(0.3518*x)+0.1181,2)              # 20/07 - 0,2/0,2 0 -> 6,2

    return round(quero, 2)                                          # Piragoras tava certo :/


def HomingAll():
    Fast.sendGCODE(arduino, "G28 Y")
    Fast.sendGCODE(arduino, "G28 X")
    Fast.G28(arduino, offset=-28)
    Fast.sendGCODE(arduino, "G28 Z")
    Fast.sendGCODE(arduino, "G92 X0 Y0 Z0 E0")
    Fast.sendGCODE(arduino, "G92.1")
    Fast.sendGCODE(arduino, "M17 X Y Z E")
    #Parafusa(132, mm=5, voltas=20)
    Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'], 1)


def verificaCLP(serial):
    global wrongSequence
    if wrongSequence >= limitWrongSequence:
        wrongSequence = 0
        Fast.sendGCODE(arduino, "M42 P36 S0")
        return 9
    echo = Fast.sendGCODE(serial, 'F', echo=True)
    echo = str(echo[len(echo)-1])
    if echo == "Comando não enviado, falha na conexão com a serial.":
        #return 4
        return "ok"
    else:
        Fast.sendGCODE(arduino, "M42 P36 S0")
    #return echo
    return "ok"

    # return strr
    #return random.choice(["ok","ok","ok","ok","ok","ok","ok","ok","ok","ok",1,"ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok",])


def Parafusa(pos, voltas=2, mm=0, ZFD=100, ZFU=100, dowLess=False, reset=False):
        Fast.M400(arduino)
        #print(pos, mm, voltas)
        Fast.sendGCODE(arduino, f'g91')
        if dowLess:
            Fast.sendGCODE(arduino, f"g38.3 Z-105 F{int(zMaxFedDown*(ZFD/100))}")
            ZFD = 50
        Fast.M400(arduino)
        
        Fast.sendGCODE(arduino, f'g38.3 z-{pos} F{int(zMaxFedDown*(ZFD/100))}')
        Fast.sendGCODE(arduino, f'g0 z{mm} F{zMaxFedUp}')
        #Fast.sendGCODE(arduino, f'm280 p{servo} s{angulo}')
        #Fast.sendGCODE(arduino, f'm43 t s10 l10 w{voltas*50}')
        #Fast.sendGCODE(arduino, f"M43 t s32 l32 w{voltas*50}")

        Fast.sendGCODE(arduino, f"M42 p32 s255")
        time.sleep(int((voltas*40/1000)))
        Fast.sendGCODE(arduino, f"M42 p32 s0")

        if reset:
            Fast.sendGCODE(arduino, "G28 Z")
        Fast.sendGCODE(arduino, 'g90')
        Fast.sendGCODE(arduino, f'g0 z{pos} F{int(zMaxFedUp*(ZFU/100))}')
        #print(f'g0 z{pos} F{int(zMaxFedUp*(ZFU/100))}')
        #Fast.M400(arduino)


def descarte(valor="Errado", Deposito={"Errado":{"X":230, "Y":0}}):
    global Total0, wrongSequence
    pos = machineParamters["configuration"]["informations"]["machine"]["defaultPosition"]["descarte"+valor]
    Fast.sendGCODE(arduino, f"G90")
    Fast.sendGCODE(arduino, f"G0 Y{pos['Y']} f{yMaxFed}")
    Fast.sendGCODE(arduino, f"G0 X{pos['X']} f{xMaxFed}")
    Fast.M400(arduino)
    Fast.sendGCODE(arduino, "M42 P31 S0")
    Fast.sendGCODE(arduino, "M42 P33 S0")
    Fast.sendGCODE(arduino, f"G0 E0 f{eMaxFed}")
    Fast.M400(arduino)
#    Fast.sendGCODE(arduino, f"G28 Y")
    cicleSeconds = round(timeit.default_timer()-Total0,1)
    asyncio.run(updateProduction(cicleSeconds, valor))
    print("updateProducion - Finish")
    if valor == "Errado" and not intencionalStop:
        wrongSequence += 1
        print(f"{Fast.ColorPrint.YELLOW}Errado: {wrongSequence}{Fast.ColorPrint.ENDC}")
    else:
        print(f"{Fast.ColorPrint.GREEN}Certo{Fast.ColorPrint.ENDC}")
        wrongSequence = 0

def timer(total):
    horas = floor(total / 3600)
    minutos = floor((total - (horas * 3600)) / 60)
    segundos = floor(total % 60)
    return f"{horas}:{minutos}:{segundos}"


def PegaObjeto():
    global Total0
    pegaPos = machineParamters['configuration']['informations']['machine']['defaultPosition']['pegaTombador']
    Total0 = timeit.default_timer()
    Fast.sendGCODE(arduino, "G90")
    Fast.sendGCODE(arduino, f"G0 X{pegaPos['X']} E0 F{xMaxFed}")
    Fast.sendGCODE(arduino, f"G0 Y{pegaPos['Y']} F{yMaxFed}")
    Fast.M400(arduino)
    Fast.sendGCODE(arduino, "M42 P31 S255")
    Fast.sendGCODE(arduino, "G4 S0.3")
    Fast.sendGCODE(arduino, "G28 Y")
#    alinhar()


def alinhar():
    alin = machineParamters['configuration']['informations']['machine']['defaultPosition']['alinhaPeca']
    Fast.sendGCODE(arduino, 'G90')
    Fast.sendGCODE(arduino, f"G0 X{alin['X']} f{xMaxFed}")
    Fast.sendGCODE(arduino, f"G0 Y{alin['Y']} f{yMaxFed}")


def Process_Imagew_Scew(frames, lower, upper, AreaMin, AreaMax, name="ScrewCuts", model="1"):
    img_draw = frames.copy()
    # cv2.imshow("img_draw_original", cv2.resize(img_draw, None, fx=0.35, fy=0.35))
    finds = 0
    for Pontos in globals()[name][model]:
        pa, pb = tuple(Pontos["P0"]), (Pontos["P0"][0]+Pontos["P1"][0],
                                       Pontos["P0"][1]+Pontos["P1"][1])

        cv2.drawMarker(img_draw, pa, (255, 50, 0), thickness=10)
        cv2.drawMarker(img_draw, pb, (50, 255, 0), thickness=10)
        cv2.rectangle(img_draw, pa, pb, (255, 50, 255), 10)
        show = frames[Pontos["P0"][1]:Pontos["P0"][1] + Pontos["P1"][1],
                   Pontos["P0"][0]:Pontos["P0"][0] + Pontos["P1"][0]]
        
        mask = Op.refineMask(Op.HSVMask(show, lower, upper), kerenelA=(10,10))
        Cnt_A, _ = Op.findContoursPlus(mask, AreaMin_A=AreaMin, AreaMax_A=AreaMax)
        
        show = cv2.bitwise_or(show, show, None, mask)
        if Cnt_A:
            finds += 1
            for info in Cnt_A:
                cv2.drawContours(show, [info['contour']], -1, (0, 255, 0), thickness=10,
                                 lineType=cv2.LINE_AA)

                for pp in range(len(info['contour'])):
                    info['contour'][pp][0] += pa[0]
                    info['contour'][pp][1] += pa[1]

                cv2.drawContours(img_draw, [info['contour']], -1, (0, 255, 0), thickness=10,
                                 lineType=cv2.LINE_AA)

        # cv2.imshow(f"Img_{Pontos}", show)
        img_draw[Pontos["P0"][1]:Pontos["P0"][1] + show.shape[0],
                Pontos["P0"][0]:Pontos["P0"][0] + show.shape[1]] = show
    cv2.putText(img_draw, str(finds), (200, 100), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 0), 10)
    # cv2.imshow(f"Draw_Copy", cv2.resize(img_draw, None, fx=0.25, fy=0.25))
    # cv2.waitKey(1)
    return img_draw, finds


def Process_Image_Hole(frame, areaMin, areaMax, perimeter, HSValues):
    img_draw = frame.copy()
    for Pontos in HoleCuts:
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #            Corta a imagem e faz as marcações               #

        show = frame[Pontos["P0"][1]:Pontos["P0"][1] + Pontos["P1"][1],
                Pontos["P0"][0]:Pontos["P0"][0] + Pontos["P1"][0]]
        pa, pb = tuple(Pontos["P0"]),(Pontos["P0"][0]+Pontos["P1"][0],
                                    Pontos["P0"][1]+Pontos["P1"][1])

        cv2.drawMarker(img_draw, pa, (255, 50, 0), thickness=10)
        cv2.drawMarker(img_draw, pb, (50, 255, 0), thickness=10)
        cv2.rectangle(img_draw, pa, pb, (255, 50, 255), 10)

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #                      Procura os furos                      #

        Resultados, R, per = findHole(show, areaMin, areaMax, perimeter, HSValues, (int((pb[0]-pa[0])/2),int((pb[1]-pa[1])/2)))

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
        #                           X-ray                            #

        img_draw[Pontos["P0"][1]:Pontos["P0"][1] + show.shape[0],
                Pontos["P0"][0]:Pontos["P0"][0] + show.shape[1]] = R

        cv2.drawMarker(img_draw, (int((pa[0]+pb[0])/2),
                                int((pa[1]+pb[1])/2)),
                                (255,0,0),
                                thickness=5,
                                markerSize=50)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                          Exibe                             #
    #cv2.imshow("show", cv2.resize(show, None, fx=0.25, fy=0.25))
    # cv2.imshow("draw", cv2.resize(img_draw, None, fx=0.25, fy=0.25))
    # cv2.waitKey(1)
    return Resultados, R, per, img_draw


def Processo_Hole(frame, areaMin, areaMax, perimeter, HSValues, ids=None, model="A", rodada=0):
    global Analise, modelo_atual
    faltadeFuro = False
    repetidos = [1, 4]
    changePos = False
    possivelErro = 0
    parafusadas = 0
    precicao = 0.42
    Reverse = False
    vazio = False
    angle = 0
    Pos = []

    path = f"Images/Process/{ids}"
    Fast.removeEmptyFolders("Images/Process")
    cameCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['camera0Centro']
    parafCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusadeiraCentro'].copy()
    parafCent['Y'] = NLinearRegression(parafCent['Y'], reverse=True)
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

    for lados in range(6):

        if vazio:
            break

        Fast.M400(arduino)
        if not intencionalStop and not faltadeFuro:
            tentativas, dsts = 0, 0
            Fast.sendGCODE(arduino, "G90")
            
            indexPos = str(int(changePos))

            Fast.sendGCODE(arduino, f"G0 X{Analise[model][str(angle)][indexPos]['X']} E{str(angle)} F{xMaxFed}")
            Fast.sendGCODE(arduino, f"G0 Y{Analise[model][str(angle)][indexPos]['Y']} F{yMaxFed}")
            Fast.M400(arduino)
            defaultCoordY = Analise[model][str(angle)][str(int(changePos))]['Y']
            atualCoordY = NLinearRegression(defaultCoordY, reverse=True)

            
            Fast.sendGCODE(arduino, "M42 P34 S255")
            Fast.sendGCODE(arduino, "G91")
            #Fast.M400(arduino)
            breakNext = False
            forceThisY = 0
            SaveY = 99

            if lados in repetidos:
                changePos = not changePos
            else:
                changePos = False
                
            while tentativas<=10 and not intencionalStop:
                if possivelErro >=3 and vazio:
                    possivelErro = 0
                    break
#                    if model == "1" or breakNext:
#                        break 
#                    elif not breakNext:
#                        model = "0.2"
#                        modelo_atual = "0.2"
#                        Fast.sendGCODE(arduino, "G90")
#                        Fast.sendGCODE(arduino, f"G0 X{Analise[model][str(angle)]['0']['X']} F{xMaxFed}")
#                        Fast.sendGCODE(arduino, f"G0 Y{Analise[model][str(angle)]['0']['Y']} F{yMaxFed}")
#                        Fast.M400(arduino)
#                        print('\n'*5)
#                        print(f"Peça invertida -> G0 X{Analise[model][str(angle)]['0']['X']}")
#                        time.sleep(1)
#                        possivelErro = 0
#                        breakNext = True
#                        tentativas = 0
#                        Reverse = True
#                        vazio = False
#
#                    else:
#                        break

                tt = timeit.default_timer()
                while timeit.default_timer()-tt <= 0.3:
                    continue
                frame = globals()['frame'+str(mainParamters["Cameras"]["hole"]["Settings"]["id"])]
                Resultados, R, per, img_draw = Process_Image_Hole(frame, areaMin, areaMax, perimeter, HSValues)
                
                # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
                #                     Verifica a distância                   #
                if Resultados:
                    vazio = False

                    if DebugPictures:
                        d = datetime.now()
                        cv2.imwrite(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/normal/L{lados}_T{tentativas}.jpg", frame)
                        cv2.imwrite(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/filtro/L{lados}_T{tentativas}.jpg", img_draw)

                    try:
                        if DebugPrint:
                            print("^^"*15)
                            print(f"Coordenada atual {defaultCoordY};  {atualCoordY}mm do 0")
                            print("Quer mover", Resultados[dsts][0],"em relação a coordenada atual")
                        MY = Resultados[dsts][0]
                        MX = Resultados[dsts][1]

                        # Calcula quantos mm tem que se mover, e soma com a posição atual, pra saber pra onde deve ir em relação ao zero
                        if (MY+atualCoordY) >= 0:
                            yReal = (MY)+atualCoordY
                        else:
                            print("Quer mover além do 0")
                            forceThisY = MY
                            yReal = 0
                            MY=0
                        if DebugPrint:
                            print("Ou seja, quer ir para: ", yReal)

                        print(f"\n AtualCoorY:{atualCoordY}\n MY:{MY}\n yReal:{yReal}\n")

                    except IndexError:
                        print("Falha de identificação, corrija o filtro..")
                        break

                    #if abs(MX) > precicao:
                    #    Fast.sendGCODE(arduino, f"G0 X{MX} F{xMaxFed}", echo=True)
                    #    
                    if abs(MY) > precicao or abs(MX) > precicao :
                        yImaginario = NLinearRegression(abs(yReal))
                        defaultCoordY = yImaginario
                        atualCoordY = yReal
                        pp = Fast.M114(arduino)
                        if DebugPrint:
                            print(f"Devera ir para coordenada {yImaginario}; {atualCoordY}mm em relação ao 0")

                        Fast.sendGCODE(arduino, f"G90")
                        Fast.sendGCODE(arduino, f"G0 Y{yImaginario} X{MX+pp['X']} F{int(yMaxFed/2)}", echo=True)
                        Fast.sendGCODE(arduino, f"G91")

                    Fast.M400(arduino)
                    time.sleep(0.5)
                    tentativas+=1

                    if DebugPrint:
                        print("Tentativa:", tentativas)

                    # Caso a precisão em ambos os eixos esteja ok, ou tnha exedido o numero de tentativas.
                    if abs(MY) <= precicao and abs(MX) <= precicao or tentativas >=9:
                        if abs(MY) <= precicao and abs(MX) <= precicao:
                            if DebugPictures:
                                d = datetime.now()
                                cv2.imwrite(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/falha/L{lados}_T{tentativas}_N.jpg", frame)
                                cv2.imwrite(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/falha/L{lados}_T{tentativas}_F.jpg", img_draw)
#                                cv2.imwrite(f"{path}/identificar/{lados}_{tentativas}_draw.jpg", img_draw)
                                #cv2.imwrite(f"{path}/identificar/{lados}_{tentativas}_normal.jpg", frame)

                            # Faz os valores ficarem acima do permiido pra evita que entre no loop novamente.
                            MY, MX, tentativas = 99, 99, 50
                            posicao = Fast.M114(arduino)
                            print('\n')
                            print(f"model:{model}, angle:{angle}, index:{str(int(changePos))}",posicao['X'], posicao['Y'], "vs", Analise[model][str(angle)][str(int(changePos))]['X'], Analise[model][str(angle)][str(int(changePos))]['Y'])
                            print('\n')
#                            Analise[model][str(angle)][str(int(changePos))]['X'] = posicao['X']
#                            Analise[model][str(angle)][str(int(changePos))]['Y'] = posicao['Y']
    
                            Pos.append(posicao)

                            # Ajusta define a coordenada do centro com base na distância da camera e da parafusadeira
                            posicao = {
                                'X':-round(cameCent['X']-posicao['X'], 2)+parafCent['X'],
                                'Y':-round((cameCent['Y']-posicao['Y'])+forceThisY, 2)+parafCent['Y'],
                                'E':posicao['E']
                            } 
                            
                            # Vai até a coordenada
                            Fast.sendGCODE(arduino, 'g90')
                            Fast.sendGCODE(arduino, f"g0 X{posicao['X']} E{posicao['E']} F{xMaxFed}")
                            Fast.sendGCODE(arduino, f"g0 Y{posicao['Y']} F{yMaxFed}")
                            if DebugPrint:
                                print(f"Parafusando em: X{posicao['X']} E{posicao['E']} Y{posicao['Y']} F{xMaxFed}" )
                            # Parafusa
                            
                            Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'],  parafusaCommand['mm'], zFRPD2, zFRPU2)
                            if angle+90 < 360:
                                if lados not in repetidos:
                                    Fast.sendGCODE(arduino, f"G0 X{Analise[model][str(angle+90)][indexPos]['X']} E{str(angle+90)} F{xMaxFed}")
                                else:
                                    Fast.sendGCODE(arduino, f"G0 X{Analise[model][str(angle+90)][indexPos]['X']} F{xMaxFed}")
                                Fast.sendGCODE(arduino, f"G0 Y{Analise[model][str(angle+90)][indexPos]['Y']} F{yMaxFed}")
                            Fast.M400(arduino)
#                            Fast.sendGCODE(arduino, f"g0 Y{1} F{yMaxFed}")
                            if globals()["pecaReset"] >= 3:
                                Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'], 1, reset=True)
                                globals()["pecaReset"] = 0
                            else:
                                Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'], 1)
                            parafusadas +=1
                        else:
                            faltadeFuro = True
                            break
                    else:
                         time.sleep(0.2)
#                        cv2.imwrite(f"{path}/identificar/Errado_R{rodada}_L{lados}_T{tentativas}_draw.jpg", img_draw)
#                        cv2.imwrite(f"{path}/identificar/Errado_R{rodada}_L{lados}_T{tentativas}_normal.jpg", frame)
                else:
                    if DebugPictures:
                        d = datetime.now()
                        cv2.imwrite(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/falha/L{lados}_T{tentativas}_NE.jpg", frame)
                        cv2.imwrite(f"{path}_{str(d.day)+str(d.month)}/identificar/{rodada}/falha/L{lados}_T{tentativas}_FE.jpg", img_draw)
                    vazio = True
                    tentativas+=1
                    possivelErro += 1
            #identificar.append(timeit.default_timer()-tI0)G0 G91
            #print("Passando pro lado:", lados+1)
            if lados not in repetidos:
#                Fast.sendGCODE(arduino, f"G91")
#                Fast.sendGCODE(arduino, f"G0 E90 F{eMaxFed}")
                angle += 90
#                Fast.M400(arduino)

    #identificar = sum(identificar)
    #print("Busca finalizada")
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

async def checkUpdate(branch="Auto_Pull"):
    subprocess.run(["git", "checkout", branch])
    subprocess.run(["git", "fetch"])
    if "Your branch is behind" in str(subprocess.check_output(["git", "status"])):
        print("Algumas alterações foram detectadas, atualizando..")
        subprocess.run(["git", "pull"])
        resp = str(subprocess.check_output(["git", "log", "-1", "--oneline"]))
        logRequest({
            "code":resp[2:9],
            "description":f"[Auto_Update]: {resp[9:len(resp)-3]}",
            "listed":False,
            "type":"info"
        })
    else:
        print("Você já está rodando a ultima versão disponivel")


async def sendParafusa(parms):
    Parafusa(parafusaCommand['Z'], parafusaCommand['voltas'],  parafusaCommand['mm'])


async def shutdown_raspberry():
    subprocess.run(["reboot"])
    await asyncio.sleep(1)


async def restart_raspberry():
    subprocess.run(["reboot"])
    await asyncio.sleep(1)


async def popupTigger(parm):
    if parm != "None":
        try:
            fun =eval(parm)
            await fun()
        except NameError:
            pass


async def refreshJson():
    global maxFeedP, maxFeedrate, stopReasons, nonStopCode, xMaxFed, yMaxFed, zMaxFedDown, zMaxFedUp, eMaxFed, zFRPD2, zFRPU2, parafusaCommand, Analise
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

    allJS={
        "allJsons":{
            "mainParamters":mainParamters,
            "machineParamters":machineParamters,
            "HoleCuts":HoleCuts,
            "ScrewCuts":ScrewCuts,
            "Analise": Analise
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
    Fast.sendGCODE(arduino, "M42 P36 S0")
    intencionalStop = True
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
        new_logs ={
            "code":new_log['code'], 
            "description":new_log['description'],
            "type":new_log['type'],
            "date":int(round(datetime.now().timestamp()))
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
    #await sendWsMessage("update", machineParamters)
    return


async def logRefresh(timeout=1):
    global logList
    date = int(round(datetime.now().timestamp()))

    M=int(datetime.fromtimestamp(date).strftime("%m"))
    Y=int(datetime.fromtimestamp(date).strftime("%Y"))
    D=int(datetime.fromtimestamp(date).strftime("%d"))

    month = datetime.fromtimestamp(date).strftime("%m")
    for log in logList['log']:
        logDate = datetime.fromtimestamp(log['date']).strftime("%m")
        if logDate != month:
            lM=int(datetime.fromtimestamp(log['date']).strftime("%m"))
            lY=int(datetime.fromtimestamp(log['date']).strftime("%Y"))
            lD=int(datetime.fromtimestamp(log['date']).strftime("%d"))
            if M-lM >=timeout and D-lD<=0:
                logList['log'].remove(log)
            Fast.writeJson('Json/logList.json', logList)


async def startAutoCheck(date=None):
    global arduino, nano, conexaoStatusArdu, conexaoStatusNano, threadStatus, infoCode 
    if date and platform.system() == "Linux":
        subprocess.run(["date", "-s", f"{date[:len(date)-len('(Horário Padrão de Brasília)')]}"])
    # await updateSlider('Normal')
    await sendWsMessage("update", machineParamters)
    await sendWsMessage("update", production)
    setCameraFilter()
    await logRefresh()
    await refreshJson()
    AutoCheckStatus = True
    connection = {
        "connectionStatus": "Tentantiva de conexão identificada"
    }

    await asyncio.sleep(0.1)
    await sendWsMessage("update", connection)

    connection["connectionStatus"] = "Conectando sistemas internos..."
    await sendWsMessage("update", connection)
    await asyncio.sleep(0.1)

    if not conexaoStatusArdu:
        connection["connectionStatus"] = "Conectando com a estação de montagem..."
        await sendWsMessage("update", connection)
        await asyncio.sleep(0.1)
        try:
            status, code, arduino = Fast.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')
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
            infoCode=5

    if not conexaoStatusNano:
        connection["connectionStatus"] = "Conectando com o CLP..."
        await sendWsMessage("update", connection)
        await asyncio.sleep(0.1)
        try:
            status_nano, code_nano, nano = Fast.SerialConnect(SerialPath='Json/serial.json', name='Nano')
            if status_nano:
                conexaoStatusNano = True
            else:
                raise TypeError 
        except TypeError:
            connection["connectionStatus"] = "Falha ao conectar com o CLP!!!"
            await sendWsMessage("update", connection)
            await asyncio.sleep(1.5)
            conexaoStatusNano = False
            infoCode = 4

    if not threadStatus:
        connection["connectionStatus"] = "Inicializando cameras..."
        await sendWsMessage("update", connection)
        await asyncio.sleep(0.1)
        try:
            globals()["thread"+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])] = CamThread(str(mainParamters["Cameras"]["screw"]["Settings"]["id"]), mainParamters["Cameras"]["screw"])
            #stalker1 = ViewAnother(thread1, 5)
            globals()["thread"+str(mainParamters["Cameras"]["hole"]["Settings"]["id"])] = CamThread(str(mainParamters["Cameras"]["hole"]["Settings"]["id"]), mainParamters["Cameras"]["hole"])
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
                appTh.stop()
        except Exception as Exp:
            connection["connectionStatus"] = "Falha ao inicializar cameras!!!"
            await sendWsMessage("update", connection)
            await asyncio.sleep(1.5)
            threadStatus = False
            print(Exp)
    
    if not conexaoStatusArdu or conexaoStatusNano or threadStatus:
        connection["connectionStatus"] = "Problemas foram encontrados..."
        await sendWsMessage("update", connection)
        
        for item in stopReasons:
            if infoCode == item['code']:
                print(item)
                await logRequest(item)
                await sendWsMessage("error", item)
        await asyncio.sleep(0.5)
    #if not conexaoStatus or not threadStatus:
        
    connection["connectionStatus"] = "Verificação concluida"
    await sendWsMessage("update", connection)
    await logRequest()
    await sendWsMessage("startAutoCheck_success")

    return AutoCheckStatus


async def startProcess(parm):
    global modelo_atual
    qtd, only, model = parm['total'], parm['onlyCorrectParts'], str(parm['partId'])
    modelo_atual = model
    t0 = timeit.default_timer()
    NewMont = Process(qtd, Fast.randomString(tamanho=5 ,pattern=""), model=modelo_atual)
    NewMont.start()
    operation["operation"]["finished"] = False
    operation["operation"]["placed"] = 0
    operation["operation"]["total"] = qtd if qtd < 999 else 0
    await sendWsMessage("update", operation)
    await sendWsMessage("startProcess_success")
    print(f"Pedido de montagem finalizado em {int(timeit.default_timer()-t0)}s")

async def updateProduction(cicleSeconds, valor):
    print("updateProducion")
    production["production"]["today"]["total"]+=1
    production["production"]["total"]["total"]+=1
    if valor!="Errado":
        print("Valor Certo")
        production["production"]["today"]["rigth"]+=1
        production["production"]["total"]["rigth"]+=1
        
        if cicleSeconds < production["production"]["total"]["timePerCicleMin"]:
            production["production"]["total"]["timePerCicleMin"] = cicleSeconds
        elif cicleSeconds > production["production"]["total"]["timePerCicleMax"]:
            production["production"]["total"]["timePerCicleMax"] = cicleSeconds

        production["production"]["today"]["timesPerCicles"].append(cicleSeconds)
        print(">>> ", timer(cicleSeconds))
    elif not intencionalStop:
        print("Valor Errado")
        production["production"]["today"]["wrong"]+=1
        production["production"]["total"]["wrong"]+=1
    current_time  = datetime.now()
    print(f"{current_time} vs {int(production['production']['today']['day'])}")
    if int(production["production"]["today"]["day"]) != int(current_time.day):
        production["production"]["yesterday"] = production["production"]["today"]
        # Zera o dia de hoje
        production["production"]["today"] = {"day": int(current_time.day),"total": 0,"rigth": 0,"wrong": 0,"timePerCicle": 0,"timesPerCicles": []}
        production["production"]["dailyAvarege"]["week_times"].append(production["production"]["yesterday"]["timePerCicle"])
        production["production"]["dailyAvarege"]["week_total"].append(production["production"]["yesterday"]["total"])
        production["production"]["dailyAvarege"]["week_rigth"].append(production["production"]["yesterday"]["rigth"])
        production["production"]["dailyAvarege"]["week_wrong"].append(production["production"]["yesterday"]["wrong"])
        week_time = production["production"]["dailyAvarege"]["week_times"]
        week_total = production["production"]["dailyAvarege"]["week_total"]
        week_rigth = production["production"]["dailyAvarege"]["week_rigth"]
        week_wrong = production["production"]["dailyAvarege"]["week_wrong"]
        appends = {"times":week_time, "total":week_total, "rigth":week_rigth, "wrong":week_wrong}
        if week_time:
            for k, v in appends.items():
                while len(v) > 7:
                    v.pop(0)
                media =  round(sum(v) /len(v),1)
                print(k, v, media)
                production["production"]["dailyAvarege"][k] = media

    valores = production["production"]["today"]["timesPerCicles"]
    if valores:
        media =  round(sum(valores) /len(valores),1)
        production["production"]["today"]["timePerCicle"] = media
    print("Escrevendo")
    Fast.writeJson('Json/production.json', production)
    await sendWsMessage("update", production)

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
#    if DebugPrint:
#        print(25*"-")
#        print("Enviado: " + cover_msg)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                       Exec                                                           #

if __name__ == "__main__":
    app = Flask(__name__)
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                        Load-Json                           #

    mainParamters = Fast.readJson('Json/mainParamters.json')
    machineParamters = Fast.readJson('Json/machineParamters.json')
    logList = Fast.readJson('Json/logList.json')
    stopReasonsList = Fast.readJson('Json/stopReasonsList.json')
    HoleCuts = Fast.readJson("../engine_H/Json/HoleCuts.json")
    ScrewCuts = Fast.readJson("../engine_H/Json/ScrewCuts.json")
    Analise = Fast.readJson("Json/Analise.json")
    production = Fast.readJson("Json/production.json")
    parafusaCommand = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusar']
    camera = machineParamters["configuration"]["camera"]
    globals()["tempFileFilter"] = mainParamters["Filtros"]["HSV"]
    globals()["pecaReset"] = 0
    modelo_atual = "1"
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                      Json-Variables                        #

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
    nano = "lixo"
    arduino = "lixo"
    wrongSequence = 0
    limitWrongSequence = 3
    portFront = machineParamters["configuration"]["informations"]["port"]
    portBack = machineParamters["configuration"]["informations"]["portStream"]
    offSetIp = 0

    if platform.system()=="Windows":
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
        print ("IP:", ip," Host:", host)

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

    globals()["thread"+str(mainParamters["Cameras"]["screw"]["Settings"]["id"])] = CamThread(str(mainParamters["Cameras"]["screw"]["Settings"]["id"]), mainParamters["Cameras"]["screw"])
    #stalker1 = ViewAnother(thread1, 5)
    globals()["thread"+str(mainParamters["Cameras"]["hole"]["Settings"]["id"])] = CamThread(str(mainParamters["Cameras"]["hole"]["Settings"]["id"]), mainParamters["Cameras"]["hole"])
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
        #appTh.join()
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
            print("sys.reboot")
        else:
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
        websockets.serve(echo, ip, portFront))
    print(f"server iniciado em {ip}:{portFront}")
    try:
        loop = asyncio.get_event_loop()
        mainThread = Thread(target=loop.run_forever)
        mainThread.start()
        print('Started!')
        #ever = asyncio.get_event_loop()
        #ever.run_forever()
    except KeyboardInterrupt:
        print("Fechando conexão com webscokets na base da força")
        #ever.join()
        try:
            cv2.destroyAllWindows()
        except cv2.error:
            pass
        exit(200)
