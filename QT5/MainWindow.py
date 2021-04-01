# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #

# Todo:                              Verificar quais não estão mais sendo usados.                                      #

# Importa os Widgets necessários.
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QPushButton,
    QWidget,
    QDialog,
    QAction,
    QLabel
)

# Importa algumas partes de certos módulos.
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from JsonMod import JsonMod
from random import randint
from PyQt5 import QtCore
from time import sleep

# Importa os principais módulos.
import FastFunctions as Fast
import OpencvPlus as Op
import numpy as np
import serial
import json
import sys
import cv2
import os


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Variables                                                         #

# Cria Comunicação Serial
arduino = Fast.SerialConnect(name='Ramps 1.4')

# Indexação e diretorios fixos em variaveis.
imgAnalysePath = "../Images/P_ (3).jpg"
ConfigDataPath = "../Json/config.json"
blockImagePath = "Images/block.png"

# Utilização de alguns diretorios fixos com base na locazilação atual do código.
jsonpath = os.path.normpath(os.path.join(os.path.dirname(__file__), "json-data.json"))
photoPath = os.path.normpath(os.path.join(os.path.dirname(__file__), imgAnalysePath))
img = cv2.imread(photoPath)

# Leitura e armazenamento inicial dos valores de configuração principal.
with open(ConfigDataPath, 'r', encoding='utf-8') as config_json_file:
    configData = json.load(config_json_file)

# Clonagem dos dados de configuração principal, para salvamento temporário.
with open(ConfigDataPath, 'r', encoding='utf-8') as temp_json_file:
    tempData = json.load(temp_json_file)

# Definição dos Nomes dos Processos
aProcess = configData["Filtros"]["HSV"]["0"]["Application"]
bProcess = configData["Filtros"]["HSV"]["1"]["Application"]
cProcess = configData["Filtros"]["HSV"]["2"]["Application"]
zProcess = "Normal"

nominalIndex = aProcess
Processo = True

# Definição dos modos/janelas do processo
Tabs = []
for Tab in configData['Mask_Parameters']:
    Tabs.append(Tab)
Tabs.append(zProcess)

# Criação de variaveis globais
marker_s = False
cap = False

column = 1
line = 1

# Definindo a localização do ponto de referência.
# Todo: Identificar ponto de referência na imagem.
pFB = (100, 60)
pFA = (50, 50)
fixPoint = (pFB[0], int(pFA[1] + ((pFB[1] - pFA[1]) / 2)))

# Corte da Imagem na área de interesse central
Quadrants = Op.meshImg(img)
img = Quadrants[line][column]


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Functions                                                         #

# Procura por padroes circulares na mascara oferecida.
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


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                 Window Classes                                                       #

# Janela "Controle da Maquina" para movimentação e ajustes de coordenadas.
class MachineController(QWidget):

    # Define o LayOut e a(s) ação(es) de cada gatilho(s).
    def __init__(self):
        super(MachineController, self).__init__()
        loadUi("Ui/machineController.ui", self)
        self.Voltar.clicked.connect(lambda checked: self.hide())
        self.PhotoPath.setText(photoPath)
        self.LigarC.clicked.connect(self.onClicked)
        self.Snapshot.clicked.connect(self.takePicture)
        self.Markers.clicked.connect(
            lambda checked: self.onClicked(True)
        )

        self.LedR.valueChanged.connect(
            lambda checked: self.SerialMonitor(
                Fast.sendGCODE(arduino,
                             "M150 R{0} U{1} B{2}".format(self.LedR.value(), self.LedG.value(), self.LedB.value()),
                             echo='True')
            )
        )

        self.LedG.valueChanged.connect(
            lambda checked: self.SerialMonitor(
                Fast.sendGCODE(arduino,
                             "M150 R{0} U{1} B{2}".format(self.LedR.value(), self.LedG.value(), self.LedB.value()),
                             echo='True')
            )
        )

        self.LedB.valueChanged.connect(
            lambda checked: self.SerialMonitor(
                Fast.sendGCODE(arduino,
                             "M150 R{0} U{1} B{2}".format(self.LedR.value(), self.LedG.value(), self.LedB.value()),
                             echo='True')
            )
        )

        self.Serial_Send.clicked.connect(
            lambda checked: self.SerialMonitor(Fast.sendGCODE(arduino, (self.Serial_In.text()).upper(), echo=True))
        )

        self.X.clicked.connect(
            lambda checked: self.moveMachine(self.X)
        )
        self.Y.clicked.connect(
            lambda checked: self.moveMachine(self.Y)
        )
        self.Z.clicked.connect(
            lambda checked: self.moveMachine(self.Z)
        )
        self.E.clicked.connect(
            lambda checked: self.moveMachine(self.E)
        )
        self.x.clicked.connect(
            lambda checked: self.moveMachine(self.x)
        )
        self.y.clicked.connect(
            lambda checked: self.moveMachine(self.y)
        )
        self.z.clicked.connect(
            lambda checked: self.moveMachine(self.z)
        )
        self.e.clicked.connect(
            lambda checked: self.moveMachine(self.e)
        )

    # Salva a vista atual da camera no caminho descrito no campo "photoPath".
    def takePicture(self):
        cv2.imwrite(str(self.PhotoPath.text()), img)

    # Movimenta o eixo passado no parametro "value", com os valores do campos na tela de configuração.
    def moveMachine(self, value):
        control = {"X": self.XN, "Y": self.YN, "Z": self.ZN, "E": self.EN}
        if str(value.objectName()).isupper():
            Func = lambda fd, dm: 'G0 ' + str(value.objectName()) + str(dm) + ' F' + str(fd)
            control[str(value.objectName())].display(control[str(value.objectName())].value() + self.dstMov.value())
        else:
            Func = lambda fd, dm: 'G0 ' + str(value.objectName()).upper() + '-' + str(dm) + ' F' + str(fd)
            control[str(value.objectName()).upper()].display(
                control[str(value.objectName()).upper()].value() - self.dstMov.value())
        self.Serial_In.setText(Func(self.FRt.value(), self.dstMov.value()))
        self.SerialMonitor(Fast.sendGCODE(arduino, Func(self.FRt.value(), self.dstMov.value()), echo=True))

    # Inicia a captura e exibição da imagem da camera principal.
    def onClicked(self, marker):
        global cap, marker_s, img
        if marker:
            if marker_s:
                marker_s = False
            else:
                marker_s = True
        elif not cap:
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(3, 1280)
            cap.set(4, 720)
            self.LigarC.setText("Desligar câmera")
            if cap.isOpened():
                while cap.isOpened():
                    _, img = cap.read()
                    if marker_s:
                        cv2.drawMarker(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)),
                                       (self.LedB.value(), self.LedG.value(), self.LedR.value()), markerSize=50,
                                       thickness=1)
                    self.displayImage(img, 1)
                    cv2.waitKey(1)
        else:
            cap.release()
            cap = False
            img = cv2.imread(blockImagePath)
            self.LigarC.setText("Ligar câmera")
            while not cap:
                self.displayImage(img, 1)
                cv2.waitKey(1)

    # Exibe o Ultimo comando e sua resposta na aba "Monitor Serial".
    def SerialMonitor(self, gcode):
        retorno = ""
        prefix = '\n' + "(send) " + (self.Serial_In.text()).upper() + ('\n' * 2)
        for linha in gcode:
            retorno = retorno + linha + '\n'
        self.Serial_Out.setText(prefix + retorno)

    # Função conversão e exibição as imagem de np.array(B,G,R) para jpg(R,G,B)
    def displayImage(self, img, window=1):
        qformat = QImage.Format_Indexed8
        imgs = cv2.resize(img, (1280, 720))
        if len(imgs.shape) == 3:
            if (imgs.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        imgs = QImage(imgs, imgs.shape[1], imgs.shape[0], qformat)
        imgs = imgs.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(imgs))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


# Janela "Json" para edição dos arquivos json.
class JsonTree(QWidget):

    # Define o LayOut e a(s) ação(es) de cada gatilho(s).
    def __init__(self):
        super(JsonTree, self).__init__()
        loadUi("Ui/jsonViwer.ui", self)

        self.view = JsonMod.QtWidgets.QTreeView()
        self.model = JsonMod.QJsonModel()

        with open(jsonpath) as f:
            self.model.load(json.load(f))

        self.view.setModel(self.model)

        self.savebtw.clicked.connect(self.saveData)
        self.TrewView()
        self.loadPath.setText(jsonpath)
        self.load.clicked.connect(self.loadpath)

    # Exibe o arquivo json carregado na memória.
    def TrewView(self):
        self.view.setColumnWidth(0, int(self.label.width() / 2))
        self.vt.addWidget(self.view)

    # Salvar os dados editados na aba de edição.
    def saveData(self):
        bkp = self.model.json()
        with open(jsonpath, 'w', encoding='utf-8') as jsonFile2:
            json.dump(bkp, jsonFile2, indent=4)

    # Carrega de outro arquivo na aba de visualização.
    def loadpath(self):
        global jsonpath
        if os.path.isfile(self.loadPath.text()) and (self.loadPath.text()).endswith('.json'):
            jsonpath = self.loadPath.text()
            with open(jsonpath) as f:
                self.model.load(json.load(f))

            self.view.setModel(self.model)


# Janela "Principal" para ajuste dos filtros, salvar valores.
class MainWindow(QMainWindow):

    # Define o LayOut e a(s) ação(es) de cada gatilho(s).
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Ui/mainWindow.ui", self)

        # Associando as classes de outras janelas a um objeto correspondente.
        self.window1 = JsonTree()
        self.window2 = MachineController()
        self.window3 = PopUp()

        # Variaveis internas da classe principal referente a orientação da modo de identificação.
        self.TabIndex = 1
        self.janela = Tabs[self.TabIndex]

        # Associação dos gatilhos à funções internas e/ou externas.
        self.SaveActualConfig.clicked.connect(self.PreSaveData)
        self.actionSair.triggered.connect(self.quit_trigger)
        self.Stop.clicked.connect(self.quit_trigger)
        self.LiveS.clicked.connect(self.onClicked)

        self.actionJson_Editor.triggered.connect(lambda checked: self.toggle_window(self.window1))
        self.actionMachine.triggered.connect(lambda checked: self.toggle_window(self.window2))
        self.actionCam.triggered.connect(lambda checked: self.toggle_window(self.window3))
        self.Next.clicked.connect(lambda checked: self.EditIndex('+'))
        self.Prev.clicked.connect(lambda checked: self.EditIndex('-'))

        # Cria uma lista com todos os slides de configuração da camera, com base no arquivo de configuração.
        self.Sliders = []
        Cam_Prop = configData["Cameras"]["Hole"]["Properties"]
        for prop in Cam_Prop:
            self.Sliders.append(getattr(self, prop))

        # Atualização dos valores de configuração com base no modo atual.
        self.LoadData()

        # Conecta cada slider de configuração da camera à função que realiza a configuração, passando os valores certos.
        for prop in range(len(self.Sliders)):
            self.Sliders[prop].valueChanged.connect(
                lambda value=self.Sliders[prop], name=self.Sliders[prop].objectName(): self.setProperties(name, value)
            )

            self.Sliders[prop].sliderReleased.connect(
               self.PreSaveData
            )

        # Conecta as caixas de seleção das cameras à função que altera a instância da camera com base no processo.
        self.IndexCA.clicked.connect(lambda checked: self.Photo(aProcess))
        self.IndexCB.clicked.connect(lambda checked: self.Photo(cProcess))

        # Conecta o botão de inicio á execução do programa de identificação.
        self.Start.clicked.connect(
            lambda checked: self.onClicked(True)
        )

        # Conecta o botão de Saida com a função que finaliza a execução do programa.
        self.Stop.clicked.connect(
            lambda checked: self.onClicked(False)
        )

    # Todo: Deixa a função setProperties estática para usa-la em outras janelas.
    # Atualiza os propriedades da camera (brilho, contraste, exposição e etc).
    def setProperties(self, a, b):
        global cap
        try:
            cap.set(getattr(cv2, 'CAP_PROP_' + a), b)
        except AttributeError:
            print(f"{Fast.ColorPrint.ERROR}O atributo {a[0]+a[1::].lower()} não pode ser definido para {b}.")
            print(f"{Fast.ColorPrint.WARNING}O novo valor do atributo {a[0]+a[1::].lower()} não sera salvo."'\n')
            pass

    # Tira uma foto com a camera desejada e salva o id da ultima camera utilizada.
    def Photo(self, id, release=True):
        if not isinstance(id, int):
            # Define o nome da camera com base no processo que é utilizada.
            camera_name = (configData["Filtros"]["HSV"][str(configData["Cameras"][id]["Settings"]["id"])]["Application"])
            # Define a mensagem de erro
            cant_read_cam_message = f"Camera do processo {camera_name} não pode ser lida."

            global cap, img, nominalIndex

            # Tenta desconectar a camera caso a mesma jpa esteja em uso.
            try:
                if cap.isOpened(): cap.release()
            except AttributeError:
                pass

            # Cria instância uma das multiplas cameras com base no processo a ser utilizado.
            cap = cv2.VideoCapture(configData["Cameras"][id]["Settings"]["id"], cv2.CAP_DSHOW)
            __, imgtemp = cap.read()

            # Verifica se a camera foi aberta, e se a mesma não encontra-se coberta e/ou sem imagem.
            try:
                if __ and cv2.countNonZero(cv2.cvtColor(imgtemp, cv2.COLOR_BGR2GRAY)) > 5000:
                    _, img = cap.read()

            # Avisa que a camera não pode ser aberta, ou encontra-se obstruida.
                else:
                    print(f"{Fast.ColorPrint.ERROR}{cant_read_cam_message}")
                    print(f"{Fast.ColorPrint.WARNING}Verifique as conexões USB"'\n')
            except cv2.error:
                print(f"{Fast.ColorPrint.ERROR}{cant_read_cam_message}")
                print(f"{Fast.ColorPrint.WARNING}Verifique as conexões USB"'\n')

            # Verifica se não está em modo stream e se deve fechar a conexão com a mesma.
            if release and not self.LiveS.isChecked():
                cap.release()

            # Atribui o endereço da camera a uma variável publica.
            nominalIndex = configData["Cameras"][id]["Settings"]["id"]

    # Vinculado os gatilhos "Next" e "Prev", altera o valor do modo/janela atual
    def EditIndex(self, parm):

        # Volta ao modo/janela anterior.
        if parm == '-':
            if self.TabIndex == 0:
                self.TabIndex = len(Tabs) - 1
            else:
                self.TabIndex = self.TabIndex - 1

        # Avançar ao proximo modo/janela.
        else:
            if self.TabIndex == len(Tabs) - 1:
                self.TabIndex = 0
            else:
                self.TabIndex = self.TabIndex + 1

        # Atualiza o modo/janela atual
        self.janela = Tabs[self.TabIndex]

        # Carrega as informações dos controles de acordo com o mesmo.
        self.LoadData()

    # Atualiza os valores de configuração com base no modo atual.
    def LoadData(self):
        if self.janela != zProcess:
            for slider in self.Sliders:
                slider.setValue(int(configData["Cameras"][self.janela]["Properties"][slider.objectName()]))

            self.h_min.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['lower'][0])
            self.s_min.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['lower'][1])
            self.v_min.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['lower'][2])
            self.h_max.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['upper'][0])
            self.s_max.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['upper'][1])
            self.v_max.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['upper'][2])
            self.A1.setValue(configData["Mask_Parameters"][self.janela]["areaMin"])
            self.A2.setValue(configData["Mask_Parameters"][self.janela]["areaMax"])

    # Salva de forma temporaria quaisquer alterações nos valores de configuração
    def PreSaveData(self):
        if self.janela != zProcess:
            for slider in self.Sliders:
                tempData["Cameras"][self.janela]["Properties"][slider.objectName()] = slider.value()

            tempData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['lower'][0] = self.h_min.value()
            tempData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['lower'][1] = self.s_min.value()
            tempData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['lower'][2] = self.v_min.value()
            tempData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['upper'][0] = self.h_max.value()
            tempData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['upper'][1] = self.s_max.value()
            tempData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['upper'][2] = self.v_max.value()
            tempData["Mask_Parameters"][self.janela]["areaMin"] = int(self.A1.value())
            tempData["Mask_Parameters"][self.janela]["areaMax"] = int(self.A2.value())

    # Executa o código de identificação com base no modo atual
    def onClicked(self, FDs):
        global cap, img, nominalIndex, Processo
        Processo = FDs
        if Processo:
            last = self.janela

            # Verifica se deve acionar a camera em modo permanente.
            if self.LiveS.isChecked():
                global cap
                # Tenta desconectar caso já exista uma conexão na variavel "cap".
                try:
                    cap.release()
                except AttributeError:
                    pass

                # Cria uma nova instância de camera na variável cap de modo permanente.
                self.Photo(nominalIndex, release=False)

            # Mantem o processo rodando.
        while Processo:

            # Atualiza a imagem em tempo real, se necessário.
            if self.LiveS.isChecked():
                if last != self.janela:

                    # Se a janela mudar, muda a instância da camera para conhecido com o processo de reconhecimento.
                    if cap.isOpened(): cap.release()
                    nominalIndex = cProcess if self.janela == cProcess or self.janela == bProcess else aProcess
                    self.Photo(nominalIndex, release=False)
                    last = self.janela

                # Atualiza a imagem
                _, img = cap.read()

            # Caso o modo seja "Normal"
            if self.janela == zProcess:
                # Desenha apenas uma marcação no centro da imagem, para orientação e ajustes rápidos.
                cv2.drawMarker(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)), (255, 0, 255), thickness=2)
                chr_k = img

            # Caso o modo seja aProcess
            if self.janela == aProcess:

                # Coleta os valores de configuração e cria um filtro personalizado
                X1, X2, X3, X4 = self.A1.value(), self.A2.value(), self.A3.value(), self.A4.value()
                imgAnalyse = img
                lower = np.array([
                    self.h_min.value(),
                    self.s_min.value(),
                    self.v_min.value()
                ])
                upper = np.array([
                    self.h_max.value(),
                    self.s_max.value(),
                    self.v_max.value()
                ])
                mask = Op.refineMask(Op.HSVMask(imgAnalyse, lower, upper))
                chr_k = cv2.bitwise_and(imgAnalyse, imgAnalyse, mask=mask)
                distances = []

                # Utliza-se do filtro criado para procurar por marcações circulares na imagem
                edge = findCircle(mask, X1, X2, X3)

                # Para cada marcação encontrada, traça marcas de orientação a sua volta.
                for Circle in edge:

                    # Desenha um circulo em volta do centro do contorno encontrado.
                    cv2.circle(chr_k, (
                        int(Circle['center'][0]),
                        int(Circle['center'][1])
                    ), int(Circle['radius']), (36, 255, 12), 2)

                    # Desenha uma linha vertical até o ponto fixo.
                    cv2.line(chr_k, (
                        int(Circle['center'][0]),
                        int(Circle['center'][1])
                    ), fixPoint, (168, 50, 131))

                    # Desenha uma linha horizontal até o ponto fixo.
                    cv2.line(chr_k, (
                        int(Circle['center'][0]),
                        fixPoint[1]
                    ), fixPoint, (0, 0, 255), thickness=2)

                    # Desenha uma linha diagonal até o ponto fixo.
                    cv2.line(chr_k, (
                        int(Circle['center'][0]),
                        int(Circle['center'][1])
                    ), (int(Circle['center'][0]), fixPoint[1]), (255, 0, 0))

                    # Calcula a distância ente o centro e o ponto fixo.
                    distance_to_fix = (
                        round((Circle['center'][0] - fixPoint[0]), 3),
                        round((Circle['center'][1] - fixPoint[1]), 3)
                    )

                    # Escreve a distância horizontal.
                    cv2.putText(chr_k, str(distance_to_fix[1]), (
                        int(Circle['center'][0]),
                        int(Circle['center'][1] / 2)
                    ), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                    # Escreve a distância vertical.
                    cv2.putText(chr_k, str(distance_to_fix[0]), (
                        int(Circle['center'][0] / 2),
                        int(fixPoint[1])
                    ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                    # Salva a distância em uma lista para uso futuro.
                    distances.append([distance_to_fix])

            # Caso o modo seja cProcess ou bProcess, referentes ao processo de identificação do parafuso.
            if self.janela == cProcess or self.janela == bProcess:

                # Coleta e define dados da imagem a ser processada
                Image = imgAnalyse = img
                width = int(Image.shape[1])
                height = int(Image.shape[0])
                offset_screw = 0.00

                #  Caso seja o Processo "Edge" (primeira etapa), busca na borda da imagem a altura de referência.
                if self.janela == bProcess:
                    edge_analyze = imgAnalyse[0:height, 0:int(width * 0.25)]
                    chr_k = imgAnalyse

                # Coleta os valores de configuração e cria um filtro personalizado
                lower = np.array([
                    self.h_min.value(),
                    self.s_min.value(),
                    self.v_min.value()
                ])
                upper = np.array([
                    self.h_max.value(),
                    self.s_max.value(),
                    self.v_max.value()
                ])
                msk = Op.refineMask(Op.HSVMask(edge_analyze, lower, upper))
                cv2.rectangle(msk, (0, 0), (msk.shape[1], msk.shape[0]), (0, 0, 0), thickness=20)
                chr_k = cv2.bitwise_and(edge_analyze, edge_analyze, mask=msk)

                # Utliza-se do filtro criado para encontrar a borda de comparação de altura do parafuso
                edge, null = Op.findContoursPlus(msk, AreaMin_A=self.A1.value(),
                                                 AreaMax_A=self.A2.value())

                # De acordo com o contorno encontrado, faz a marcação correspondente.
                if edge:
                    for info_edge in edge:
                        cv2.drawContours(chr_k, [info_edge['contour']], -1, (70, 255, 20), 3)

                        # Se for a primeira etapa, redefine a imagem de analize com base nos valores encontrados
                        if self.janela == bProcess:
                            point_a = tuple(info_edge['contour'][0])
                            edge_analyze = imgAnalyse[point_a[1]: height, 0:width]

                        # Se for a segunda etapa, realiza as marcações adequadas.
                        if self.janela == cProcess:
                            offset_screw = round(info_edge['dimension'][0], 3)
                            cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 255, 255), thickness=3)

            # Exibe a Imagem
            self.displayImage(chr_k, 1)
            cv2.waitKey(1)

            # Todo: Salvar de forma temporária somente quando algum valor mudar.
            # self.PreSaveData()

    # Função conversão e exibição as imagem de np.array(B,G,R) para jpg(R,G,B)
    def displayImage(self, imgs, window=1):
        qformat = QImage.Format_Indexed8
        if self.janela == zProcess and not self.LiveS.isChecked():
            imgs = cv2.resize(imgs, None, fx=0.25, fy=0.25)
        if len(imgs.shape) == 3:
            if (imgs.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        imgs = QImage(imgs, imgs.shape[1], imgs.shape[0], qformat)
        imgs = imgs.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(imgs))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    # Sai do aplicativo, e em caso de mudanças pergunta se deseja salva-las
    def quit_trigger(self):
        global Processo
        Processo = False
        if tempData != configData:
            self.toggle_window(self.window3)
            # for jan in Tabs:
            #     self.janela = jan
            #     if self.janela != zProcess:
            #         print('~~' * 30)
            #         for slider in self.Sliders:
            #             print(self.janela, slider.objectName(),
            #                   tempData["Cameras"][self.janela]["Properties"][slider.objectName()])
            #         print('~~' * 15)
            #         for slider in self.Sliders:
            #             print(self.janela, slider.objectName(),
            #                   configData["Cameras"][self.janela]["Properties"][slider.objectName()])
            # sys.exit(500)
        else:
            # for jan in Tabs:
            #     self.janela = jan
            #     if self.janela != zProcess:
            #         print('~~'*30)
            #         print("TempData")
            #         for slider in self.Sliders:
            #             print(self.janela, slider.objectName(),
            #                   tempData["Cameras"][self.janela]["Properties"][slider.objectName()])
            #         print('~~' * 15)
            #         print("dataConfig")
            #         for slider in self.Sliders:
            #             print(self.janela, slider.objectName(),
            #                   configData["Cameras"][self.janela]["Properties"][slider.objectName()])
            sys.exit(200)

    # Troca entre as janelas existentes.
    def toggle_window(self, window):
        if window.isVisible():
            window.hide()

        else:
            if window.windowTitle() == self.window2.windowTitle():
                window.showFullScreen()
            else:
                window.show()


# Janela "PopUp" para confirmação de alteração permanente nos dados.
class PopUp(QDialog):

    # Define o LayOut e a(s) ação(es) de cada gatilho(s).
    def __init__(self):
        super(PopUp, self).__init__()
        loadUi("Ui/Popup.ui", self)
        self.nao.clicked.connect(lambda checked: self.quit_trigger(199))
        self.sim.clicked.connect(lambda checked: self.Save(201))

    # Salva o arquivo temporario no logar do arquivo original.
    def Save(self, exit_C=None):
        try:
            with open(ConfigDataPath, "w", encoding='utf-8') as configSave_json_file:
                json.dump(tempData, configSave_json_file, indent=4)
        except OSError as erroGrave:
            print(f"{Fast.ColorPrint.ERROR}Não foi possível salvar o arquivo, tente novamente.")
            print(f"{Fast.ColorPrint.WARNING}As edições não foram salvas. Entre em contato com a manutenção."'\n')
            print(f"{Fast.ColorPrint.BLUE}[TEMP_FILE]: {tempData}{Fast.ColorPrint.ENDC}"'\n')
            print(f"{Fast.ColorPrint.ERROR}Falha encontrada:")
            print(f"{Fast.ColorPrint.ERROR}{erroGrave}")
        if exit_C:
            self.quit_trigger(exit_C)

    # Sai da aplicação e mantem os arquivos originais.
    def quit_trigger(self, exit_code=200):
        sys.exit(exit_code)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                  Code Execution                                                      #

# Definição da instância do aplicativo.
app = QApplication(sys.argv)

# Correlação da Janela Principal com a primeira janela a ser exibida
w = MainWindow()
w.showMaximized()

# Para a execução do aplicativo caso o mesmo retorne algum código de erro.
sys.exit(app.exec_())
