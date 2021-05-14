from flask import Flask, Response, request, jsonify
import FastFunctions as Fast
import OpencvPlus as Op
import numpy as np
import threading
import socket
import cv2



"""
# Clico de Configuração
    # Extrai os valores do JSON
    # Estabelece conexão com o Mega
    # Alinha os motores

# Ciclo Continuo
    #  Ciclo que mexe o motor de Pega. ( Vai, Estica, Retrai, Volta )  # Posições Fixas
    #  4x Analisa/Salva/Roda
    #  4X Corrige com base nas informações armazenadas
    #  inverte o array
    #  4x MexeP/Posição, Desce Parafusando uma quantidade fixa
    #  -> 'N'x /Analisa/Corrige/Parafusa no sentido Contrario
    #  -> Roda
"""


class CamThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self._running = True

        self.mainConfig = fullJson
        self.HSVJson = self.mainConfig['Filtros']['HSV']
        self.Processos = ['Edge', 'Screw']
        self.HSVjsonIndex = 0

        self.HSVValues_Hole = self.HSVJson[str(self.HSVjsonIndex)]['Valores']
        self.Process_Values = self.mainConfig['Mask_Parameters']['Hole']

        self.pFA = (50, 50)
        self.pFB = (100, 60)
        self.fixPoint = (self.pFB[0], int(self.pFA[1] + ((self.pFB[1] - self.pFA[1]) / 2)))

        for values in self.Process_Values:
            self.__dict__[values] = self.Process_Values[values]

    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

    def frameNormal(self):
        while True:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                   + cv2.imencode('.JPEG', globals()['frame'+self.previewName],
                                  [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                   + b'\r\n')

    def frameScrew(self):
        while True:
            _, frame = findScrew(globals()['frame'+self.previewName], self.HSVJson, self.mainConfig, self.Processos)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                   + cv2.imencode('.JPEG', frame,
                                  [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                   + b'\r\n')

    def frameHole(self):
        while True:
            dst, frame = findHole(globals()['frame' + self.previewName], self.areaMin, self.areaMax, self.perimeter, self.HSVValues_Hole, self.fixPoint)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'
                   + cv2.imencode('.JPEG', frame,
                                  [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                   + b'\r\n')


def camPreview(previewName, camID):
    cam = cv2.VideoCapture(camID, cv2.CAP_DSHOW)  # Abre a camera com o id passado.
    # cam.set(3, 1280*2)
    # cam.set(4, 720*2)
    if cam.isOpened():                            # Verifica se foi aberta
        rval, frame = cam.read()                  # Lê o Status e uma imagem
    else:
        rval = False

    while rval:                                   # Verifica e camera ta 'ok'
        rval, frame = cam.read()                  # Atualiza
        globals()[f'frame{previewName}'] = frame  # Exporta
        cv2.imshow(previewName, frame)  # Exibe
        key = cv2.waitKey(1)  # Espera
        # yield frame

        if key == 27:
            break
    cv2.destroyWindow(previewName)


def findHole(imgAnalyse, minArea, maxArea, c_perimeter, HSValues, fixed_Point):
    if type(imgAnalyse) != np.ndarray:
        print(type(imgAnalyse))
        imgAnalyse = Op.takeSnapshot(imgAnalyse)

    for filter_values in HSValues:
        locals()[filter_values] = np.array(Op.extractHSValue(HSValues, filter_values))
    mask = Op.refineMask(Op.HSVMask(imgAnalyse, locals()['lower'], locals()['upper']))
    chr_k = cv2.bitwise_and(imgAnalyse, imgAnalyse, mask=mask)
    distances = []
    edge = findCircle(mask, minArea, maxArea, c_perimeter)
    for Circle in edge:
        cv2.circle(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])), int(Circle['radius']),
                   (36, 255, 12), 2)

        cv2.line(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])), fixed_Point, (168, 50, 131))

        cv2.line(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])),
                 (int(Circle['center'][0]), fixed_Point[1]), (255, 0, 0))

        cv2.line(chr_k, (int(Circle['center'][0]), fixed_Point[1]), fixed_Point, (0, 0, 255), thickness=2)

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
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    edges = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    edges = edges[0] if len(edges) == 2 else edges[1]
    for c in edges:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        area = cv2.contourArea(c)
        if len(approx) > perimeter_size and areaMinC < area < areaMaxC:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            circle_info.append({"center": (x, y), "radius": r})
    return circle_info


def findScrew(imgAnalyse, FiltrosHSV, MainJson, processos, bh=0.3):
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
        for key in keys:
            locals()[key] = Op.extractHSValue(value, key)
        msk = Op.refineMask(Op.HSVMask(edge_analyze, locals()['lower'], locals()['upper']))
        cv2.rectangle(msk, (0, 0), (msk.shape[1], msk.shape[0]), (0, 0, 0), thickness=20)
        chr_k = cv2.bitwise_and(edge_analyze, edge_analyze, mask=msk)
        edge, null = Op.findContoursPlus(msk,
                                         AreaMin_A=MainJson['Mask_Parameters'][aba]['areaMin'],
                                         AreaMax_A=MainJson['Mask_Parameters'][aba]['areaMax']
                                         )

        if edge:
            for info_edge in edge:
                cv2.drawContours(chr_k, [info_edge['contour']], -1, (70, 255, 20), 3)
                if aba == processos[0]:
                    point_a = tuple(info_edge['contour'][0])
                    edge_analyze = imgAnalyse[point_a[1]: height, 0:width]
                    pass
                if aba == processos[1]:
                    offset_screw = round(info_edge['dimension'][0], 3)
                    cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (255, 255, 255), thickness=3)
        else:
            return offset_screw, chr_k
    return offset_screw, chr_k


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


if __name__ == "__main__":
    app = Flask(__name__)
    fullJson = Fast.readJson('Json/config.json')

    thread1 = CamThread("1", 1)
    thread0 = CamThread("0", 0)
    thread1.start()
    thread0.start()

    @app.route('/')
    def homepage():
        return 'App vem Aqui?.'

    @app.route('/exit', methods=['GET'])
    def shutdown():
        shutdown_server()

        print("Esperando Threads Serem Finalizadas")
        thread0.join()
        thread1.join()
        print("Threads Finalizadas com sucesso.")

        return 'Server shutting down...'


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
        return Response(getattr(globals()['thread'+str(id)], "frame"+valor)(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    #
    # @app.route('/0')
    # def video_feed0():
    #     return Response(thread0.frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # Fica preso até a camera ser iniciada
    # e uma imagem existir em uma das variaveis globais

    while True:
        try:
            if type(globals()['frame1']) ==  np.ndarray:
                break
        except KeyError:
            continue

    offSetIp = 0
    port = 5050
    prefix = socket.gethostbyname(socket.gethostname()).split('.')
    ip = '.'.join(['.'.join(prefix[:len(prefix) - 1]), str(int(prefix[len(prefix) - 1]) + offSetIp)])

    app.run(host=ip, port=port, debug=True, threaded=True, use_reloader=False)




    #
    # Process = 'Holeasadadw'
    # pathImages = '../Images/'
    # Read = 'A3.jpg' if Process == 'Hole' else 'P_ (3).jpg'
    # Process = 'Hole'
    # Image = cv2.imread(pathImages + Read)
    # Quadrants = Op.meshImg(Image)
    #
    # line = 1
    # column = 1
    # Image = Quadrants[line][column]
    #
    # mainConfig = Fast.readJson('Json/config.json')
    # HSVJson = mainConfig['Filtros']['HSV']
    # Processos = ['Edge', 'Screw']
    # HSVjsonIndex = 0
    #
    # HSVValues_Hole = HSVJson[str(HSVjsonIndex)]['Valores']
    # Process_Values = mainConfig['Mask_Parameters'][str(Process)]
    #
    # for values in Process_Values:
    #     locals()[values] = Process_Values[values]
    #
    # pFA = (50, 50)
    # pFB = (100, 60)
    # fixPoint = (pFB[0], int(pFA[1] + ((pFB[1] - pFA[1]) / 2)))
    #
    # T0A = timeit.default_timer()
    #
    # # Exibe o conteúdo da variavel 'frame1'
    # while True:
    #     _, img = findHole(globals()['frame1'], areaMin, areaMax, perimeter, HSVValues_Hole, fixPoint)
    #     _, img2 = findScrew(Image, HSVJson, mainConfig, Processos)
    #     print(_)
    #     cv2.imshow('A', img)
    #     cv2.imshow('B', img2)
    #     #     key = cv2.waitKey(1)
    #     if key == 27:
    #         break
    #
    # # Finaliza as threads.
    # cv2.destroyWindow("A")
    # cv2.destroyWindow("B")
    #
    #
    # # Resultados = [findHole(Image, areaMin, areaMax, perimeter, HSVValues_Hole, fixPoint),
    # #               findScrew(Image, HSVJson, mainConfig, Processos)]
    # print("Tempo de Execução:", round(timeit.default_timer() - T0A, 3))

