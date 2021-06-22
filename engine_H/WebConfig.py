# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
# Nota: Use Crtl + Shift + -    para colapsar todo o código e facilitar a visualização.
#
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #

from flask import Flask, Response, request, jsonify
import FastFunctions as Fast
import OpencvPlus as Op
import numpy as np
import threading
import socket
import cv2

import websockets
import asyncio
import socket
import json

import timeit

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                      JSON                                                            #

ws_message = {
    "command": "",
    "parameter": ""
}

"""
    def frameNormal(self):
    while not self.stopped() and self.Procs['Normal']:
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                + cv2.imencode('.JPEG', globals()['frame'+self.previewName],
                                [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                + b'\r\n')
    print("Quebrou Normal")

    def frameScrew(self):
        while not self.stopped() and self.Procs['Normal']:
            _, frame = findScrew(
                self. imgTeste, fullJson['Filtros']['HSV'], fullJson, self.Processos)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                   + cv2.imencode('.JPEG', frame,
                                  [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                   + b'\r\n')
        print("Quebrou Screw")

    def frameEdge(self):
        while not self.stopped() and self.Procs['Edge']:
            _, frame = findScrew(
                self. imgTeste, fullJson['Filtros']['HSV'], fullJson, self.Processos, aba=0)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                   + cv2.imencode('.JPEG', frame,
                                  [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                   + b'\r\n')
        print("Quebrou Edge")



    def frameScrew(self):
        while True:
            _, frame = findScrew(globals()[
                                 'frame'+self.previewName], fullJson['Filtros']['HSV'], fullJson, self.Processos)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                   + cv2.imencode('.JPEG', frame,
                                  [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                   + b'\r\n')

    def frameEdge(self):
        while True:
            _, frame = findScrew(globals()[
                                 'frame'+self.previewName], fullJson['Filtros']['HSV'], fullJson, self.Processos, aba=0)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                   + cv2.imencode('.JPEG', frame,
                                  [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                   + b'\r\n')

    def frameHole(self):
        while not self.stopped() and self.Procs['Hole']:
            _, frame = findHole(globals()['frame' + self.previewName], self.areaMin,
                                self.areaMax, self.perimeter, self.HSVValues_Hole, self.fixPoint)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                   + cv2.imencode('.JPEG', frame,
                                  [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                   + b'\r\n')
        print("Quebrou Hole")
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

        self.mainConfig = fullJson
        self.HSVJson = self.mainConfig['Filtros']['HSV']
        self.Processos = ['Edge', 'Screw']
        self.HSVjsonIndex = 'Hole'

        self.HSVValues_Hole = self.HSVJson[str(self.HSVjsonIndex)]['Valores']
        self.Process_Values = self.mainConfig['Mask_Parameters']['Hole']

        self.pFA = (50, 50)
        self.pFB = (100, 60)
        self.fixPoint = (self.pFB[0], int(
            self.pFA[1] + ((self.pFB[1] - self.pFA[1]) / 2)))
        # self. imgTeste = (Op.meshImg(cv2.imread(r'.\Images\P_ (3).jpg')))[1][1]
        for values in self.Process_Values:
            self.__dict__[values] = self.Process_Values[values]

        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        print("Starting " + self.previewName)
        return self.camPreview(self.previewName, self.camID)
        
    def camPreview(self, previewName, camID):
        # Abre a camera com o id passado.
        cam = cv2.VideoCapture(camID)
        cam.set(3, 1280)
        cam.set(4, 720)

        if cam.isOpened():                            # Verifica se foi aberta
            rval, frame = cam.read()                  # Lê o Status e uma imagem
        else:
            globals()[f'frame{previewName}'] = cv2.imread(f"../engine_H/Images/{camID}.jpg")
            rval = False

        while rval and not self.stopped():                                   # Verifica e camera ta 'ok'
            rval, frame = cam.read()                  # Atualiza
            globals()[f'frame{previewName}'] = frame
            cv2.imshow(f'frame{previewName}', frame)  # Exporta
            if cv2.waitKey(1) == 27:
                break
        try:    
            cv2.destroyWindow(previewName)
        except cv2.error:
            pass
        cam.release()
        print("Saindo da thread", self.previewName)
        return False


    def ViewCam(self):
        while not self.stopped():
            if self.Procs['Edge']:
                _, frame = findScrew(globals()[
                                     'frame'+self.previewName], fullJson['Filtros']['HSV'], fullJson, self.Processos, aba=0)
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                       + b'\r\n')
            if self.Procs['Screw']:
                _, frame = findScrew(globals()[
                                     'frame'+self.previewName], fullJson['Filtros']['HSV'], fullJson, self.Processos)
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                       + cv2.imencode('.JPEG', frame,
                                      [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                       + b'\r\n')
            if self.Procs['Hole']:
                _, frame = findHole(globals()['frame' + self.previewName], self.areaMin,
                                    self.areaMax, self.perimeter, self.HSVValues_Hole, self.fixPoint)
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

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Functions                                                         #

def findHole(imgAnalyse, minArea, maxArea, c_perimeter, HSValues, fixed_Point):
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
    for Circle in edge:
        cv2.circle(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])), int(Circle['radius']),
                   (36, 255, 12), 2)

        cv2.line(chr_k, (int(Circle['center'][0]), int(
            Circle['center'][1])), fixed_Point, (168, 50, 131))

        cv2.line(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])),
                 (int(Circle['center'][0]), fixed_Point[1]), (255, 0, 0))

        cv2.line(chr_k, (int(Circle['center'][0]), fixed_Point[1]),
                 fixed_Point, (0, 0, 255), thickness=2)

        distance_to_fix = (round((Circle['center'][0] - fixed_Point[0]), 3),
                           round((Circle['center'][1] - fixed_Point[1]), 3))
        cv2.putText(chr_k, str(distance_to_fix[1]), (int(Circle['center'][0]), int(Circle['center'][1] / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.putText(chr_k, str(distance_to_fix[0]), (int(Circle['center'][0] / 2), int(fixed_Point[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        distances.append([distance_to_fix])
    return distances, chr_k


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
    for c in edges:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        area = cv2.contourArea(c)
        if len(approx) > perimeter_size and areaMinC < area < areaMaxC:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            circle_info.append({"center": (x, y), "radius": r})
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


def shutdown_server():
    shutdown_function = request.environ.get('werkzeug.server.shutdown')
    if shutdown_function is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_function()

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                 Async-Functions                                                      #

async def updateSlider(processos):
    Config['configuration']['camera']['process'] = processos
    for x in Config['configuration']['camera']:
        if x[0:1] != 'p':
            Config['configuration']['camera'][x] = [
                fullJson['Filtros']['HSV'][processos]['Valores']['lower'][x[0:1]+'_min'],
                fullJson['Filtros']['HSV'][processos]['Valores']['upper'][x[0:1]+'_max']
            ]

    await sendWsMessage("update", Config)


async def funcs():
    pass


async def startAutoCheck():
    await updateSlider('Normal')
    await sendWsMessage("startAutoCheck_success")

    global StartedStream
    if not StartedStream:
        thread1.start()
        thread0.start()
        while True:
            try:
                if type(globals()['frame1']) == np.ndarray:
                    break
            except KeyError:
                continue

        appTh.start()
        print("Transmissão de vídeo iniciada.")
        StartedStream = True


async def updateFilter(zipped):
    for xx in fullJson["Filtros"]["HSV"]:
        if zipped['process'] in fullJson["Filtros"]["HSV"][xx]["Application"]:
            # fullJson["Filtros"]["HSV"][xx]["Valores"]["lower"][zipped[1].key()] = [zipped[1]]
            min = list(zipped.keys())[1]
            max = list(zipped.keys())[2]
            print(fullJson["Filtros"]["HSV"][xx]["Valores"]
                  ["lower"][min], '-> ', zipped[min])
            print(fullJson["Filtros"]["HSV"][xx]["Valores"]
                  ["upper"][max], '-> ', zipped[max])
            fullJson["Filtros"]["HSV"][xx]["Valores"]["lower"][min] = zipped[min]
            fullJson["Filtros"]["HSV"][xx]["Valores"]["upper"][max] = zipped[max]


async def saveJson():
    Fast.writeJson('Json/Temp.json', fullJson)
    print("salvei")


async def sendWsMessage(command, parameter=None):
    global ws_message
    ws_message["command"] = command
    ws_message["parameter"] = parameter

    # ident deixa o objeto mostrando bonito
    cover_msg = json.dumps(ws_message, indent=2)
    await ws_connection.send(cover_msg)
    print(25*"-")
    print("Enviado: " + cover_msg)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                       Exec                                                           #

if __name__ == "__main__":
    app = Flask(__name__)
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                        Load-Json                           #

    fullJson = Fast.readJson('Json/config.json')
    Config = Fast.readJson('Json/machine.json')

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                        Variables                           #

    StartedStream = False
    AP = True

    portFront = 5000
    portBack = 5050
    offSetIp = 0

    prefix = socket.gethostbyname(socket.gethostname()).split('.')
    ip = '.'.join(['.'.join(prefix[:len(prefix) - 1]),
                  str(int(prefix[len(prefix) - 1]) + offSetIp)])



    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                      Start-Threads                         #

    thread1 = CamThread("1", fullJson["Cameras"]["Screw"]["Settings"]["id"])
    thread0 = CamThread("0", fullJson["Cameras"]["Hole"]["Settings"]["id"])
    appTh = AppThread(ip, portBack)
    

    if AP:
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                          Routes                            #

        @app.route('/')
        def homepage():
            return 'App vem Aqui?.'

        @app.route('/exit', methods=['GET'])
        def shutdown():
            print("Pediu pra parar.")
            thread0.stop()
            thread1.stop()
            shutdown_server()
            print("Esperando Threads Serem Finalizadas")
            thread0.join()
            thread1.join()
            appTh.join()
            print("Threads Finalizadas com sucesso.")
            return "Server Fechado"

        @app.route('/config', methods=['GET', 'POST'])
        def all_data():
            if request.method == 'POST':
                post_data = request.get_json()
                print(post_data)
            return jsonify({
                'status': 'success',
                'Config': fullJson
            })

        @app.route('/<valor>/<id>') 
        def video_feed(valor, id):
            Esse = getattr(globals()['thread'+str(id)], "Procs")
            for processo in Esse:
                Esse[processo] = True if processo == valor else False
            print("Chamando...")
            return Response(getattr(globals()['thread'+str(id)], "ViewCam")(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                    Inside-Async-Def                        #

        async def sendGcode(obj):
            #Fast.sendGCODE(arduino, str(obj))
            print("Gcode:" + obj)
            return

        async def actions(message):
            # Verifica se afunção requisita existe e executa.
            command = message["command"]
            try:
                funcs = eval(command)
                try:
                    await funcs(message["parameter"])
                except KeyError:
                    await funcs()
            except NameError:
                print(command+"() não é uma função válida.")

        async def echo(websocket, path):
            global ws_connection
            ws_connection = websocket
            async for message in ws_connection:
                print(json.loads(message))
                await actions(json.loads(message))

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
    #                      Server-Start                          #

        asyncio.get_event_loop().run_until_complete(
            websockets.serve(echo, ip, portFront))

        print(f"server iniciado em {ip}:{portFront}")

        try:
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            print("Fechando conexão com webscokets na base da força")
            try:
                cv2.destroyAllWindows()
            except cv2.error:
                pass
            exit(200)
    
    else:
        thread1 = CamThread("1", 1)
        thread0 = CamThread("0", 0)
        thread1.start()
        thread0.start()
        while True:
            try:
                if type(globals()['frame1']) == np.ndarray:
                    break
            except KeyError:
                continue

        Process = 'Hole'
        pathImages = '.\Images'
        Read = '\A3.jpg' if Process == 'Hole' else '\P_ (3).jpg'
        Process = 'Hole'
        Image = cv2.imread(pathImages + Read)
        Quadrants = Op.meshImg(Image)

        line = 1
        column = 1
        Image = Quadrants[line][column]

        mainConfig = Fast.readJson('Json/config.json')
        HSVJson = mainConfig['Filtros']['HSV']
        Processos = ['Edge', 'Screw']
        HSVjsonIndex = 'Hole'

        HSVValues_Hole = HSVJson[str(HSVjsonIndex)]['Valores']
        Process_Values = mainConfig['Mask_Parameters'][str(Process)]

        for values in Process_Values:
            locals()[values] = Process_Values[values]

        pFA = (50, 50)
        pFB = (100, 60)
        fixPoint = (pFB[0], int(pFA[1] + ((pFB[1] - pFA[1]) / 2)))

        T0A = timeit.default_timer()

        # Exibe o conteúdo da variavel 'frame1'
        while True:
            _, img = findHole(Image, areaMin, areaMax, perimeter, HSVValues_Hole, fixPoint)
            _, img2 = findScrew(Image, HSVJson, mainConfig, Processos)
            cv2.imshow('A', img)
            cv2.imshow('B', img2)
            key = cv2.waitKey(1)
            if key == 27:
                break

        # Finaliza as threads.
        # cv2.destroyWindow("A")
        # cv2.destroyWindow("B")

        # Resultados = [findHole(Image, areaMin, areaMax, perimeter, HSVValues_Hole, fixPoint),
        #               findScrew(Image, HSVJson, mainConfig, Processos)]
        print("Tempo de Execução:", round(timeit.default_timer() - T0A, 3))
 