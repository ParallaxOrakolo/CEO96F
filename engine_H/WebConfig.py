# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
# Nota: Use Crtl + Shift + -    para colapsar todo o código e facilitar a visualização.
#
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #

from FastFunctions import MyException
from flask import Flask, Response, request, jsonify
from datetime import datetime
import FastFunctions as Fast
import OpencvPlus as Op
from threading import Thread
import numpy as np
import subprocess
import websockets
import threading
import platform
import asyncio
import socket
import random
import socket
import time
import json
import cv2
import os
import timeit
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                      JSON                                                            #

ws_message = {
    "command": "",
    "parameter": ""
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

        self.Procs = {"Hole": False, "Edge": False,
                      "Screw": False, "Normal": False}

        self.Processos = ['Edge', 'Screw']
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
            if self.Procs['Edge']:
                _, frame = findScrew(globals()[
                                     'frame'+self.previewName], mainParamters['Filtros']['HSV'], mainParamters, self.Processos, aba=0)
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                       + b'\r\n')
            if self.Procs['Screw']:
                
                frame, _ = Process_Imagew_Scew(
                                    globals()['frame'+self.previewName],
                                    Op.extractHSValue(mainParamters['Filtros']['HSV']['Screw']["Valores"], 'lower' ),
                                    Op.extractHSValue(mainParamters['Filtros']['HSV']['Screw']["Valores"], 'upper' ),
                                    mainParamters['Mask_Parameters']['Screw']['areaMin'],
                                    mainParamters['Mask_Parameters']['Screw']['areaMax']
                                    )
                # _, frame = findScrew(globals()[
                #                      'frame'+self.previewName], mainParamters['Filtros']['HSV'], mainParamters, self.Processos)
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                       + b'\r\n')
            if self.Procs['Hole']:
                _, _, _, frame = Process_Image_Hole(
                    globals()['frame' + self.previewName],
                    mainParamters['Mask_Parameters']['Hole']['areaMin'],
                    mainParamters['Mask_Parameters']['Hole']['areaMax'],
                    mainParamters['Mask_Parameters']['Hole']['perimeter'],
                    mainParamters['Filtros']['HSV']['Hole']['Valores']
                    )
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                       + b'\r\n')
            if self.Procs['Normal']:
                # print("Normal")
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', globals()['frame'+self.previewName],
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
    def __init__(self, quantidad, id):
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

        self.id = id
        self.cor = getattr(Fast.ColorPrint, random.choice(["YELLOW", "GREEN", "BLUE", "RED"]))

    def run(self):
        self.preMount()
        self.Mount()
        self.posMount()

    def preMount(self):

        print(f"{self.cor} ID:{self.id}--> pre Mount Start{Fast.ColorPrint.ENDC}")

        print(f"Foi requisitado a montagem de {self.qtd} peças certas.")

        
        self.cameCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['camera0Centro']
        self.parafCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusadeiraCentro']

        self.intervalo = {
                    'X':self.parafCent['X']-self.cameCent['X'],
                    'Y':self.parafCent['Y']-self.cameCent['Y']
                    }

        print(f"{self.cor} ID:{self.id}--> pre Mount Finish{Fast.ColorPrint.ENDC}")

    def Mount(self):

        self.infoCode = verificaCLP(nano)
        while self.qtd != self.corretas and not intencionalStop:
            self.rodada +=1

            # ------------ Vai ate tombador e pega ------------ #
            try:
                PegaObjeto()
            except MyException as Mye:
                print(Mye)
                break

            # ------------ Acha as coordenadas parciais do furo ------------ #
            parcialFuro = Processo_Hole(None,
                        mainParamters['Mask_Parameters']['Hole']['areaMin'],
                        mainParamters['Mask_Parameters']['Hole']['areaMax'],
                        mainParamters['Mask_Parameters']['Hole']['perimeter'],
                        mainParamters['Filtros']['HSV']['Hole']['Valores'])


            # ------------ Vai ate tombador e pega ------------ #
            self.infoCode = verificaCLP(nano)
            if self.infoCode in nonStopCode and not intencionalStop:
                if len(parcialFuro) >= 5: # Verificar qual o número certo .....
                    montar = []
                    tM0 = timeit.default_timer()
                    finalFuro = []
                    for posicao in parcialFuro:
                        print("Posicao: ", posicao)
                        print(-round(self.cameCent['X']-posicao['X'], 2), self.intervalo['X'])

                        # ------------ Acha a posição final dos furos  ------------ #
                        finalFuro.append({
                                    'X':-round(self.cameCent['X']-posicao['X'], 2)+self.parafCent ['X'],
                                    'Y':-round(self.cameCent['Y']-posicao['Y'], 2)+self.parafCent['Y'],
                                    'E':posicao['E']} )

                    # ------------ Roda a sequência de parafusar ------------ #
                    Fast.sendGCODE(arduino, 'g90')
                    for posicao in finalFuro:
                        self.infoCode = verificaCLP(nano)
                        if self.infoCode in nonStopCode and not intencionalStop:
                            Fast.sendGCODE(arduino, f"g0 X{posicao['X']} E{posicao['E']} F{xMaxFed}")
                            Fast.sendGCODE(arduino, f"g0 Y{posicao['Y']} F{yMaxFed}")
                            Parafusa(160, mm=0, voltas=20)
                            Fast.sendGCODE(arduino, f"g0 Y{1} F{yMaxFed}")
                            Parafusa(160, mm=0, voltas=20)
                            montar.append(timeit.default_timer()-tM0)
                        else:
                            print("Prolema encontado durante o processo de parafusar")
                            break
                    
                    # ------------ Verifica se a montagme está ok ------------ #
                    if self.infoCode in nonStopCode and not intencionalStop:
                        montar=sum(montar)
                        print("Montagem finalizada.")
                        print("Iniciando processo de validação.")
                        Fast.sendGCODE(arduino, "G90")
                        Fast.sendGCODE(arduino, "G28 Y")
                        Fast.sendGCODE(arduino, "G0 X 230")
                        validar = timeit.default_timer()
                        _, encontrados = Process_Imagew_Scew(
                                            globals()['frame'+str(mainParamters["Cameras"]["Screw"]["Settings"]["id"])],
                                            Op.extractHSValue(mainParamters['Filtros']['HSV']['Screw']["Valores"], 'lower' ),
                                            Op.extractHSValue(mainParamters['Filtros']['HSV']['Screw']["Valores"], 'upper' ),
                                            mainParamters['Mask_Parameters']['Screw']['areaMin'],
                                            mainParamters['Mask_Parameters']['Screw']['areaMax']
                                            )
                        validar = timeit.default_timer()-validar
                        if encontrados == 6:
                            descarte("Certo")
                            self.corretas+=1
                        else:
                            print(f"Foram fixados apenas {encontrados} parafusos.")
                            #descarte("Errado")
                            self.erradas+=1
                    else:
                        print("Problema encontrado antes de validar a montagem")
                        break
                else:
                    print("Problema encontrado depois do processo de Scan ")
                    print(f"Foram econtrados apenas {len(parcialFuro)} furos.")
                    #descarte("Errado")
                    self.erradas+=1
            else:
                print("Prolema encontado antes de iniciar o processo de Scan")
                break 

            print(f"{self.cor} ID:{self.id}--> {self.rodada}{Fast.ColorPrint.ENDC}")

    def posMount(self):
        print(f"{self.cor} ID:{self.id}--> POS Mount Start{Fast.ColorPrint.ENDC}")
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
                if 20 <= int(info_edge['dimension'][0]/2) <= 80:

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


def NLinearRegression(x):
    return round((0.0059*(x**2)) + (0.2741*x) + (0.6205), 2)


def HomingAll():
    Fast.sendGCODE(arduino, "G28 Y")
    Fast.sendGCODE(arduino, "G28 X")
    Fast.G28(arduino)
    Fast.sendGCODE(arduino, "G28 Z")
    Fast.sendGCODE(arduino, "G92 X0 Y0 Z0 E0")
    Fast.sendGCODE(arduino, "G92.1")
    Parafusa(160, mm=5, voltas=20)


def verificaCLP(serial):
    echo = Fast.sendGCODE(serial, 'F', echo=True)
    echo = str(echo[len(echo)-1])
    if echo == "Comando não enviado, falha na conexão com a serial.":
        #return 4
        return "ok"
    #return echo
    return "ok"

    # return strr
    #return random.choice(["ok","ok","ok","ok","ok","ok","ok","ok","ok","ok",1,"ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok","ok",])


def Parafusa(pos, voltas=2, mm=0, servo=0, angulo=0):
        Fast.M400(arduino)
        Fast.sendGCODE(arduino, f'g91')
        Fast.sendGCODE(arduino, f'g38.3 z-{pos} F{zMaxFed}')
        Fast.sendGCODE(arduino, f'g0 z-{mm} {zMaxFed}')
        Fast.sendGCODE(arduino, f'm280 p{servo} s{angulo}')
        #Fast.sendGCODE(arduino, f'm43 t s10 l10 w{voltas*50}')
        Fast.sendGCODE(arduino, f"M43 t s32 l32 w{voltas*50}")
        Fast.sendGCODE(arduino, 'g90')
        Fast.sendGCODE(arduino, f'g0 z{pos} F{1200}')
        Fast.M400(arduino)


def descarte(valor="Errado", Deposito={"Errado":{"X":230, "Y":0}}):
    pos = machineParamters["configuration"]["informations"]["machine"]["defaultPosition"]["descarte"+valor]
    Fast.sendGCODE(arduino, f"G90")
    Fast.sendGCODE(arduino, f"G0 Y{pos['Y']} f{yMaxFed}")
    Fast.sendGCODE(arduino, f"G0 X{pos['X']} f{xMaxFed}")
    Fast.M400(arduino)
    Fast.sendGCODE(arduino, "M42 P31 S0")
    Fast.sendGCODE(arduino, "M42 P33 S0")
    Fast.sendGCODE(arduino, f"G28 Y")


def PegaObjeto():
    print("Indo pegar...")
    pegaPos = machineParamters['configuration']['informations']['machine']['defaultPosition']['pegaTombador']
    anlPos = machineParamters['configuration']['informations']['machine']['defaultPosition']['analisaFoto']
    Fast.sendGCODE(arduino, "G90")
    Fast.sendGCODE(arduino, f"G0 X{pegaPos['X']} E0 F{xMaxFed}")
    Fast.sendGCODE(arduino, f"G0 Y{pegaPos['Y']} F{yMaxFed}")
    Fast.M400(arduino)
    Fast.sendGCODE(arduino, "M42 P31 S255")
    Fast.sendGCODE(arduino, "G4 S0.3")
    Fast.sendGCODE(arduino, "G28 Y")
    Fast.sendGCODE(arduino, f"G0 X{anlPos['X']} F{xMaxFed}")
    Fast.sendGCODE(arduino, f"G0 Y{anlPos['Y']} F{yMaxFed}")
    Fast.M400(arduino)
    Fast.sendGCODE(arduino, "M42 P34 S255")
    Fast.sendGCODE(arduino, "G91")
    print("Pegou")


def Process_Imagew_Scew(frames, lower, upper, AreaMin, AreaMax ):
    print("Validando encaixe....")
    img_draw = frames.copy()
    # cv2.imshow("img_draw_original", cv2.resize(img_draw, None, fx=0.35, fy=0.35))
    finds = 0
    for Pontos in ScrewCuts:
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
    print("Feito")
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


def Processo_Hole(frame, areaMin, areaMax, perimeter, HSValues):
    print("Iniciando busca pelos furos...")
    precicao = 0.4
    Pos = []
    identificar = []
    for lados in range(4):
        tentavias = 0
        dsts = 0
        tI0 = timeit.default_timer()
        while tentavias<=5:
            print("Extraindo resultados")
            frame = globals()['frame'+str(mainParamters["Cameras"]["Hole"]["Settings"]["id"])]
            Resultados, R, per, img_draw = Process_Image_Hole(frame, areaMin, areaMax, perimeter, HSValues)
            cv2.imshow("Img_Process", cv2.resize(frame, None, fx=0.3, fy=0.3))
            cv2.imshow("Fora_Hole", cv2.resize(img_draw, None, fx=0.3, fy=0.3))
            cv2.waitKey(2)
            print("Resultados:", Resultados)
            # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
            #                     Verifica a distância                   #
            if Resultados:
                try:
                    MY = Resultados[dsts][0]
                    MX = Resultados[dsts][1]
                except IndexError:
                    print("Falha de identificação, corrija o filtro..")
                    break
                print("MX:", MX, '\n MY:', MY)
#                   MX += (randint(-int(abs(MX)/4),abs(int(MX))))
                if abs(MX) > precicao:
                    Fast.sendGCODE(arduino, f"G0 X{MX} Y0 F{xMaxFed}", echo=True)
                    print(f"G0 X{MX} Y0 F{xMaxFed}")
                    
                elif abs(MY) > precicao:
                    aMY = NLinearRegression(abs(MY))
                    aMY *= -1 if MY < 0 else 1
                    Fast.sendGCODE(arduino, f"G0 X0 Y{aMY} F{yMaxFed}", echo=True)
                    print(f"G0 X0 Y{aMY} F{yMaxFed}")

                Fast.M400(arduino)
                tentavias+=1

                print("Tentativa:", tentavias)
                if abs(MY) <= precicao and abs(MX) <= precicao or tentavias >=3 :
                    Pos.append(Fast.M114(arduino))
                    if len(Resultados)>1:
                        if dsts == 0:
                            dsts += 1
                        else:
                            tentavias = 10
                    else:
                        tentavias = 10
            else:
                tentavias+=1
        identificar.append(timeit.default_timer()-tI0)
        print("Passando pro lado:", lados+1)
        Fast.sendGCODE(arduino, f"G0 E90 F{eMaxFed}")
    identificar = sum(identificar)
    print("Busca finalizada")
    return Pos

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
            "date":int(round(datetime.now().timestamp()))})
    else:
        print("Você já está rodando a ultima versão disponivel")


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
    await sendWsMessage("update", machineParamters)


async def funcs():
    pass


async def stopProcess():
    global intencionalStop
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
           await logRequest({
            "code":code,
            "description":item['description'],
            "date":date})
    
    await asyncio.sleep(0.5)


async def logRequest(new_log=False):
    global logList
    if new_log:
        logList["log"].append(new_log)
    Fast.writeJson('Json/logList.json', logList)
    await sendWsMessage("update", logList)
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


async def startAutoCheck():
    global arduino, nano, conexaoStatusArdu, conexaoStatusNano, threadStatus, infoCode 
    # await logRequest({"code":functionLog["AVI"]["code"], 
    #                   "description":functionLog["AVI"]["description"],
    #                   "date":int(round(datetime.now().timestamp()))})

    await updateSlider('Normal')
    await logRefresh()
    AutoCheckStatus = True
    connection = {
        "connectionStatus": "Tentantiva de conexão identificada"
    }

    await asyncio.sleep(0.5)
    await sendWsMessage("update", connection)

    connection["connectionStatus"] = "Conectando sistemas internos..."
    await asyncio.sleep(0.5)
    await sendWsMessage("update", connection)

    if not conexaoStatusArdu:
        try:
            status, code, arduino = Fast.SerialConnect(SerialPath='Json/serial.json', name='Ramps 1.4')
            if status:
                conexaoStatusArdu = True
                HomingAll()
            else:
                raise TypeError
        except TypeError:
            conexaoStatusArdu = False
            infoCode=5
            # await logRequest({"code":-200, 
            #                   "description":"[ERRO]: Conexão com a placa 'Ramps 1.4' não pode estabelecida.",
            #                   "date":int(round(datetime.now().timestamp()))})
    if not conexaoStatusNano:
        try:
            status_nano, code_nano, nano = Fast.SerialConnect(SerialPath='Json/serial.json', name='Nano')
            if status_nano:
                conexaoStatusNano = True
            else:
                raise TypeError 
        except TypeError:
            conexaoStatusNano = False
            infoCode = 4
            # await logRequest({"code":-200, 
            #     "description":"[ERRO]: Conexão com a placa 'Nano' não pode estabelecida.",
            #     "date":int(round(datetime.now().timestamp()))})

    # if not status:
    #     await sendWsMessage('erro', {'codigo': code, 'menssagem':arduino })
    #     AutoCheckStatus = False
    connection["connectionStatus"] = "Inicializando cameras..."
    await sendWsMessage("update", connection)
    await asyncio.sleep(0.5)
    if not threadStatus:
        try:
            thread1.start()
            # stalker1.start()
            thread0.start()
            # stalker0.start()
        
            while True:
                try:
                    if type(globals()['frame1']) == np.ndarray:
                        break
                except KeyError:
                    continue

            appTh.start()
            print("Transmissão de vídeo iniciada.")
            threadStatus = True
        except Exception as Exp:
            threadStatus = False
            print(Exp)
    
    if not conexaoStatusArdu or conexaoStatusNano or threadStatus:
        connection["connectionStatus"] = "Problema encontrado durante a conexão..."
        await sendWsMessage("update", connection)
        
        for item in stopReasons:
            if infoCode == item['code']:
                print(item)
                await logRequest({
                        "code":item['code'], 
                        "description":item['description'],
                        "date":int(round(datetime.now().timestamp()))})
                await sendWsMessage("error", item)
        await asyncio.sleep(1.5)
    #if not conexaoStatus or not threadStatus:
        
    connection["connectionStatus"] = "Verificação concluida"
    await sendWsMessage("update", connection)
    await sendWsMessage("startAutoCheck_success")

    # await logRequest({"code":functionLog["AVT"]["code"], 
    #                   "description":functionLog["AVT"]["description"],
    #                   "date":int(round(datetime.now().timestamp()))})

    return AutoCheckStatus


async def startProcess(qtd=9999):
    t0 = timeit.default_timer()
    NewMont = Process(qtd, Fast.randomString(tamanho=5 ,pattern=">>>"))
    NewMont.start()
    await sendWsMessage("startProcess_success")
    print(f"Pedido de montagem finalizado em {int(timeit.default_timer()-t0)}s")


async def startProcessss(qtd=9999):
    global intencionalStop, arduino, nano
    await sendWsMessage("startProcess_success")

    # await logRequest({"code":functionLog["PSI"]["code"], 
    #                   "description":functionLog["PSI"]["description"],
    #                   "date":int(round(datetime.now().timestamp()))})

    print(f"Foi requisitado a montagem de {qtd} peças certas.")
    time.sleep(3)
    erradas = 0
    corretas = 0
    rodada = 0
    intencionalStop = False # Destrava a maquina quando um novo processo é iniciado.
    descargaCompleta = timeit.default_timer()
    cameCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['camera0Centro']
    parafCent = machineParamters['configuration']['informations']['machine']['defaultPosition']['parafusadeiraCentro']

    intervalo = {
                'X':parafCent['X']-cameCent['X'],
                'Y':parafCent['Y']-cameCent['Y']
                }

    infoCode = "ok"
    infoCode = verificaCLP(nano)
    print(infoCode)
    #while qtd != corretas and not intencionalStop:
    for rr in range(qtd):
        if intencionalStop:
            break
        print("IntencionalStop:", intencionalStop)
        rodada +=1
        totalUnitario = timeit.default_timer()
        try:
            PegaObjeto()
        except MyException as Mye:
            print(Mye)
            break
        parcialFuro =['', '', '', '']

        # await logRequest({"code":functionLog["IDI"]["code"], 
        #               "description":functionLog["IDI"]["description"],
        #               "date":int(round(datetime.now().timestamp()))})

        parcialFuro = Processo_Hole(None,
                      mainParamters['Mask_Parameters']['Hole']['areaMin'],
                      mainParamters['Mask_Parameters']['Hole']['areaMax'],
                      mainParamters['Mask_Parameters']['Hole']['perimeter'],
                      mainParamters['Filtros']['HSV']['Hole']['Valores'])

        # await logRequest({"code":functionLog["IDT"]["code"], 
        #               "description":functionLog["IDT"]["description"],
        #               "date":int(round(datetime.now().timestamp()))})

        infoCode = verificaCLP(nano)
        print("~~"*10)
        print("604: Info code:", infoCode)
        print("~~"*10)
        if infoCode in nonStopCode:
            if len(parcialFuro) >= 5:
                print("Iniciando processo de montagem...")
                montar = []
                tM0 = timeit.default_timer()
                finalFuro = []
                for posicao in parcialFuro:
                    print("Posicao: ", posicao)
                    print(-round(cameCent['X']-posicao['X'], 2), intervalo['X'])
                    finalFuro.append({
                                'X':-round(cameCent['X']-posicao['X'], 2)+parafCent ['X'],
                                'Y':-round(cameCent['Y']-posicao['Y'], 2)+parafCent['Y'],
                                'E':posicao['E']} )

                Fast.sendGCODE(arduino, 'g90')
                for posicao in finalFuro:
                    infoCode = verificaCLP(nano)
                    print("~~"*10)
                    print("625: Info code:", infoCode)
                    print("~~"*10)
                    if infoCode in nonStopCode:
                        Fast.sendGCODE(arduino, f"g0 X{posicao['X']} E{posicao['E']} F{xMaxFed}")
                        Fast.sendGCODE(arduino, f"g0 Y{posicao['Y']} F{yMaxFed}")
                        Parafusa(160, mm=0, voltas=20)
                        #Fast.sendGCODE(arduino, f"g0 X{122} F{xMaxFed}")
                        Fast.sendGCODE(arduino, f"g0 Y{1} F{yMaxFed}")
                        Parafusa(160, mm=0, voltas=20)
                        montar.append(timeit.default_timer()-tM0)
                    else:
                        print("Prolema encontado no 625")
                        break

                if infoCode in nonStopCode:
                    montar=sum(montar)
                    print("Montagem finalizada.")
                    print("Iniciando processo de validação.")
                    Fast.sendGCODE(arduino, "G90")
                    Fast.sendGCODE(arduino, "G28 Y")
                    Fast.sendGCODE(arduino, "G0 X 230")
                    validar = timeit.default_timer()
                    _, encontrados = Process_Imagew_Scew(
                                        globals()['frame'+str(mainParamters["Cameras"]["Screw"]["Settings"]["id"])],
                                        Op.extractHSValue(mainParamters['Filtros']['HSV']['Screw']["Valores"], 'lower' ),
                                        Op.extractHSValue(mainParamters['Filtros']['HSV']['Screw']["Valores"], 'upper' ),
                                        mainParamters['Mask_Parameters']['Screw']['areaMin'],
                                        mainParamters['Mask_Parameters']['Screw']['areaMax']
                                        )
                    validar = timeit.default_timer()-validar
                    if encontrados == 6:
                        descarte("Certo")
                        corretas+=1
                    else:
                        print(f"Foram fixados apenas {encontrados} parafusos.")
                        descarte("Errado")
                        erradas+=1
                else:
                    print("Prolema encontado após 625")
                    break
            else:
                print(f"Foram econtrados apenas {len(parcialFuro)} furos.")
                descarte("Errado")
                erradas+=1
            totalUnitario = timeit.default_timer()-totalUnitario
        else:
            print("Prolema encontado no 607")
            break 
    for item in stopReasons:
        if infoCode == item['code']:
            print(f"Erro ao tentar montar a {rodada} peça")
            print(item)
            await sendWsMessage("error", item)

    descargaCompleta = timeit.default_timer()-descargaCompleta
    #intencionalStop = False
    

    # await logRequest({"code":functionLog["PST"]["code"], 
    #                   "description":functionLog["PST"]["description"],
    #                   "date":int(round(datetime.now().timestamp()))})


async def updateFilter(zipped):
    for xx in mainParamters["Filtros"]["HSV"]:
        if zipped['process'] in mainParamters["Filtros"]["HSV"][xx]["Application"]:
            # mainParamters["Filtros"]["HSV"][xx]["Valores"]["lower"][zipped[1].key()] = [zipped[1]]
            min = list(zipped.keys())[1]
            max = list(zipped.keys())[2]
            if min == "areaMin" and max == "areaMax":
                mainParamters['Mask_Parameters'][xx][min] = zipped[min]
                mainParamters['Mask_Parameters'][xx][max] = zipped[max]
                print("Update Filter:",xx,mainParamters['Mask_Parameters'][xx])
            else:
                print(mainParamters["Filtros"]["HSV"][xx]["Valores"]
                    ["lower"][min], '-> ', zipped[min])
                print(mainParamters["Filtros"]["HSV"][xx]["Valores"]
                    ["upper"][max], '-> ', zipped[max])
                mainParamters["Filtros"]["HSV"][xx]["Valores"]["lower"][min] = zipped[min]
                mainParamters["Filtros"]["HSV"][xx]["Valores"]["upper"][max] = zipped[max]
        

async def saveJson():
    Fast.writeJson('Json/config.json', mainParamters)
    print("salvei")


async def sendWsMessage(command, parameter=None):
    global ws_message
    ws_message["command"] = command
    ws_message["parameter"] = parameter

    # ident deixa o objeto mostrando bonito
    cover_msg = json.dumps(ws_message, indent=2, ensure_ascii=False)
    await ws_connection.send(cover_msg)
    print(25*"-")
    print("Enviado: " + cover_msg)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                       Exec                                                           #

if __name__ == "__main__":
    app = Flask(__name__)
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                        Load-Json                           #

    mainParamters = Fast.readJson('Json/config.json')
    machineParamters = Fast.readJson('Json/machine.json')
    logList = Fast.readJson('Json/logList.json')
    HoleCuts = Fast.readJson("../engine_H/Json/HolePoints.json")
    ScrewCuts = Fast.readJson("../engine_H/Json/ScrewPoints.json")
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                      Json-Variables                        #

    # if mainParamters["Recover"]["Status"]:
    #     mainParamters["Recover"]["Status"] = False
    #     Fast.writeJson('Json/config.json', mainParamters)
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

    xFRP = 50
    yFRP = 70
    zFRP = 100
    eFRP = 50

    maxFeedrate = machineParamters["configuration"]["informations"]["machine"]["maxFeedrate"]
    stopReasons = machineParamters["configuration"]["statistics"]["stopReasons"]
    nonStopCode = machineParamters["configuration"]["statistics"]["nonStopCode"]

    xMaxFed = int(maxFeedrate["xMax"]*(xFRP/100))
    yMaxFed = int(maxFeedrate["yMax"]*(yFRP/100))
    zMaxFed = int(maxFeedrate["zMax"]*(zFRP/100))
    eMaxFed = int(maxFeedrate["aMax"]*(eFRP/100))
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                        Variables                           #

    StartedStream = False
    intencionalStop = False
    AP = True
    nano = "lixo"
    arduino = "lixo"

    portFront = machineParamters["configuration"]["informations"]["port"]
    portBack = portFront+1
    offSetIp = 0

    if platform.system()=="Windows":
        prefix = socket.gethostbyname(socket.gethostname()).split('.')
        ip = '.'.join(['.'.join(prefix[:len(prefix) - 1]),
                  str(int(prefix[len(prefix) - 1]) + offSetIp)])
    else:
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[2], 0))
        ip = s.getsockname()[0]
        gateway = gw[2]
        host = socket.gethostname()
        print ("IP:", ip, " GW:", gateway, " Host:", host)

    machineParamters["configuration"]["informations"]["ip"] = ip
    Fast.writeJson('Json/machine.json', machineParamters)

    functionLog = machineParamters['configuration']["statistics"]["functionsCode"]

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                      Start-Threads                         #

    globals()["thread"+str(mainParamters["Cameras"]["Screw"]["Settings"]["id"])] = CamThread(str(mainParamters["Cameras"]["Screw"]["Settings"]["id"]), mainParamters["Cameras"]["Screw"])
    #stalker1 = ViewAnother(thread1, 5)
    globals()["thread"+str(mainParamters["Cameras"]["Hole"]["Settings"]["id"])] = CamThread(str(mainParamters["Cameras"]["Hole"]["Settings"]["id"]), mainParamters["Cameras"]["Hole"])
    #stalker0 = ViewAnother(thread0, 5)
    appTh = AppThread(ip, portBack)
    
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                          Routes                            #

    @app.route('/')
    def homepage():
        return 'App vem Aqui?.'

    @app.route('/exit', methods=['GET'])
    def shutdown():
        print("Pediu pra parar.")
        for x in range(10):
            try:
                globals()["thread"+str(x)].stop()
                print(f"Aguardando 'thread{str(x)}' parar..")
                globals()["thread"+str(x)].join()
                print(f"'thread{str(x)}' parou com sucesso.. \n")
            except KeyError:
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
        print("Recebeu cahmado:", message)
        command = message["command"]
        try:
            funcs = eval(command)
            try:
                await funcs(message["parameter"])
            except KeyError:
                await funcs()
        except NameError as nmr:
            print(nmr)
            print(command+"() não é uma função válida.")

    async def echo(websocket, path):
        global ws_connection
        ws_connection = websocket
        async for message in ws_connection:
            print(json.loads(message))
            await actions(json.loads(message))
            print("~~~~~~~~~~~~~~"*20)

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
