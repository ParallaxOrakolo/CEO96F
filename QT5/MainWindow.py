# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Imports                                                           #

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

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from JsonMod import JsonMod
from random import randint
from PyQt5 import QtCore

import FastFunctions as Ff
import OpencvPlus as Op
import numpy as np
import json
import sys
import cv2
import os


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Variables                                                         #

# Indexação e diretorios fixos em variaveis.
imgAnalysePath = "../Images/P_ (3).jpg"
ConfigDataPath = '../Json/config.json'
jsonpath = "json-data.json"
blockImagePath = "../Images/block.png"

photoPath = os.path.normpath(os.path.join(os.path.dirname(__file__), imgAnalysePath))
img = cv2.imread(photoPath)

# Leitura e armazenamento inicial dos valores de configuração principal.
with open(ConfigDataPath, 'r', encoding='utf-8') as config_json_file:
    configData = json.load(config_json_file)

# Clonagem dos dados de configuração principal, para salvamento temporário.
with open(ConfigDataPath, 'r', encoding='utf-8') as temp_json_file:
    tempData = json.load(temp_json_file)

# Definição dos modos de processo
Tabs = []
for Tab in configData['Mask_Parameters']:
    Tabs.append(Tab)

# Criação de variaveis globais
marker_s = False
cap = False

nominalIndex = 0
column = 1
line = 1

pFB = (100, 60)
pFA = (50, 50)
fixPoint = (pFB[0], int(pFA[1]+((pFB[1]-pFA[1])/2)))

Quadrants = Op.meshImg(img)
img = Quadrants[line][column]

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                    Functions                                                         #


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
                "M150 R{0} U{1} B{2}".format(self.LedR.value(), self.LedG.value(), self.LedB.value()))
        )

        self.LedG.valueChanged.connect(
            lambda checked: self.SerialMonitor(
                "M150 R{0} U{1} B{2}".format(self.LedR.value(), self.LedG.value(), self.LedB.value()))
        )
        self.LedB.valueChanged.connect(
            lambda checked: self.SerialMonitor(
                "M150 R{0} U{1} B{2}".format(self.LedR.value(), self.LedG.value(), self.LedB.value()))
        )

        self.Serial_Send.clicked.connect(
            lambda checked: self.SerialMonitor(self.Serial_In.text())
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

    def takePicture(self):
           cv2.imwrite(str(self.PhotoPath.text()), img)

    def moveMachine(self, value):
        control = {"X": self.XN, "Y": self.YN, "Z": self.ZN, "E": self.EN}
        if str(value.objectName()).isupper():
            Func = lambda fd, dm: 'G0 ' + str(value.objectName()) + str(dm) + ' F' + str(fd)
            control[str(value.objectName())].display(control[str(value.objectName())].value()+self.dstMov.value())
        else:
            Func = lambda fd, dm: 'G0 ' + str(value.objectName()).upper()+'-' + str(dm) + ' F' + str(fd)
            control[str(value.objectName()).upper()].display(control[str(value.objectName()).upper()].value()-self.dstMov.value())

        # Todo: Implement SendGCODE()
        print(Func(self.FRt.value(), self.dstMov.value()))

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

    def SerialMonitor(self, gcode):
        # Todo: Implementar SendGcode e WaitingEcho
        self.Serial_Out.setText(str(gcode).upper())

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

    def __init__(self):
        super(JsonTree, self).__init__()
        loadUi("Ui/jsonViwer.ui", self)
        self.savebtw.clicked.connect(self.saveData)
        self.TrewView()

    def TrewView(self):
        view.setColumnWidth(0, int(self.label.width()/2))
        self.vt.addWidget(view)

    def saveData(self):
        bkp = model.json()
        with open(jsonpath, 'w', encoding='utf-8') as jsonFile2:
            json.dump(bkp, jsonFile2, indent=4)


# Janela "Principal" para ajuste dos filtros, salvar valores.
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Ui/mainWindow.ui", self)

        # Associando as classes de outras janelas a um objeto correspondente.
        self.window1 = JsonTree()
        self.window2 = MachineController()
        self.window3 = PopUp()

        # Variaveis internas da classe principal referente a orientação da modo de identificação.
        self.janela = "Edge"
        self.TabIndex = 1

        # Associação dos gatilhos à funções internas e/ou externas.
        self.LiveS.clicked.connect(self.onClicked)
        self.Next.clicked.connect(lambda checked: self.EditIndex('+'))
        self.Prev.clicked.connect(lambda checked: self.EditIndex('-'))
        self.actionSair.triggered.connect(self.quit_trigger)
        self.Stop.clicked.connect(self.quit_trigger)
        self.actionJson_Editor.triggered.connect(lambda checked: self.toggle_window(self.window1))
        self.actionMachine.triggered.connect(lambda checked: self.toggle_window(self.window2))
        self.actionCam.triggered.connect(lambda checked: self.toggle_window(self.window3))
        self.IndexCA.clicked.connect(lambda checked: self.Photo(0))
        self.IndexCB.clicked.connect(lambda checked: self.Photo(1))
        self.Start.clicked.connect(
            lambda checked: self.onClicked(True)
        )

        self.Stop.clicked.connect(
            lambda checked: self.onClicked(False)
        )

        # Atualização dos valores de configuração com base no modo atual.
        self.LoadData()

    # Tira uma foto com a camera desejada e salva o id da ultima camera utilizada.
    def Photo(self, id, release=True):
        global cap, img, nominalIndex
        cap = cv2.VideoCapture(id, cv2.CAP_DSHOW)
        _, img = cap.read()
        if release and not self.LiveS.isChecked():
            cap.release()
        nominalIndex = id

    # Vinculado os gatilhos "Next" e "Prev", altera o valor do modo atual
    def EditIndex(self, parm):
        if parm == '-':
            if self.TabIndex == 0:
                self.TabIndex = len(Tabs)-1
            else:
                self.TabIndex = self.TabIndex - 1
        else:
            if self.TabIndex == len(Tabs)-1:
                self.TabIndex = 0
            else:
                self.TabIndex = self.TabIndex + 1
        self.janela = Tabs[self.TabIndex]
        self.LoadData()

    # Atualiza os valores de configuração com base no modo atual.
    def LoadData(self):
        self.h_min.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['lower'][0])
        self.s_min.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['lower'][1])
        self.v_min.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['lower'][2])
        self.h_max.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['upper'][0])
        self.s_max.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['upper'][1])
        self.v_max.setValue(configData['Filtros']['HSV'][str(self.TabIndex)]['Valores']['upper'][2])
        self.A1.setValue(configData["Mask_Parameters"][self.janela]["areaMin"])
        self.A2.setValue(configData["Mask_Parameters"][self.janela]["areaMax"])

    # Salva de forma temporaria quaiser alterações nos valores de configuração
    def PreSaveData(self):
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
        global cap, img, nominalIndex

        # Verifica se deve acionar a camera em modo permanente.
        if self.LiveS.isChecked():
            self.Photo(nominalIndex, release=False)

        while True:
            # Atualiza a imagem em tempo real, se necessário.
            if self.LiveS.isChecked():
                _, img = cap.read()

            # Caso o modo seja "Normal"
            if self.janela == "Normal":
                # Desenha apenas uma marcação no centro da imagem, para orientação e ajustes rápidos.
                cv2.drawMarker(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)), (255, 0, 255), thickness=2)

            # Caso o modo seja "Hole"
            if self.janela == "Hole":

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
                    cv2.circle(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])), int(Circle['radius']),
                               (36, 255, 12), 2)

                    cv2.line(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])), fixPoint, (168, 50, 131))

                    cv2.line(chr_k, (int(Circle['center'][0]), int(Circle['center'][1])),
                             (int(Circle['center'][0]), fixPoint[1]), (255, 0, 0))

                    cv2.line(chr_k, (int(Circle['center'][0]), fixPoint[1]), fixPoint, (0, 0, 255), thickness=2)

                    distance_to_fix = (round((Circle['center'][0] - fixPoint[0]), 3), round((Circle['center'][1] - fixPoint[1]), 3))
                    cv2.putText(chr_k, str(distance_to_fix[1]),
                                (int(Circle['center'][0]), int(Circle['center'][1] / 2)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                    cv2.putText(chr_k, str(distance_to_fix[0]), (int(Circle['center'][0] / 2), int(fixPoint[1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    distances.append([distance_to_fix])



            # Caso o modo seja "Screw" ou "Edge", referentes ao processo de identificação do parafuso.
            if self.janela == "Screw" or self.janela == "Edge":

                # Define e coleta e define dados da imagem a ser processada
                Image = imgAnalyse = img
                width = int(Image.shape[1])
                height = int(Image.shape[0])
                offset_screw = 0.00

                #  Caso seja o Processo "Edge" (primeira etapa)
                if self.janela == "Edge":
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
                        if self.janela == "Edge":
                            point_a = tuple(info_edge['contour'][0])
                            edge_analyze = imgAnalyse[point_a[1]: height, 0:width]

                        # Se for a segunda etapa, realiza as marcações adequadas.
                        if self.janela == "Screw":
                            offset_screw = round(info_edge['dimension'][0], 3)
                            cv2.putText(chr_k, str(offset_screw), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 255, 255), thickness=3)

                # Exibe a Imagem
                self.displayImage(chr_k, 1)
                cv2.waitKey(1)
                self.PreSaveData()

    def ShowProcess(self, color=False):
        global cap, marker_s, img
        if not cap:
            self.Start.setText("PARAR")
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(3, 1280)
            cap.set(4, 720)
            if cap.isOpened():
                while cap.isOpened():
                    _, img = cap.read()
                    if color:
                        img = cv2.cvtColor(img, color)
                    self.displayImage(img, 1)
                    cv2.waitKey(1)
        else:
            self.Start.setText("INICIAR")
            cap.release()
            cap = False
            img = cv2.imread(blockImagePath)
            while not cap:
                self.displayImage(img, 1)
                cv2.waitKey(1)

    def displayImage(self, imgs, window=1):
        qformat = QImage.Format_Indexed8
        # imgs = cv2.resize(img, None, fx=0.25, fy=0.25)
        if len(imgs.shape) == 3:
            if (imgs.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        imgs = QImage(imgs, imgs.shape[1], imgs.shape[0], qformat)
        imgs = imgs.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(imgs))
        self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def quit_trigger(self):
        if tempData != configData:
            self.toggle_window(self.window3)
        else:
            sys.exit(200)

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
    def __init__(self):
        super(PopUp, self).__init__()
        loadUi("Ui/Popup.ui", self)
        self.nao.clicked.connect(lambda checked: self.quit_trigger(199))
        self.sim.clicked.connect(lambda checked: self.Save(201))

    def Save(self, exit_C=None):
        with open(ConfigDataPath, "w", encoding='utf-8') as configSave_json_file:
            json.dump(tempData, configSave_json_file, indent=4)
        if exit_C:
            self.quit_trigger(exit_C)

    def quit_trigger(self, exit_code=200):
        sys.exit(exit_code)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#                                                  Code Execution                                                      #

app = QApplication(sys.argv)
view = JsonMod.QtWidgets.QTreeView()
model = JsonMod.QJsonModel()

with open(jsonpath) as f:
    model.load(json.load(f))

view.setModel(model)

w = MainWindow()
w.showMaximized()
sys.exit(app.exec_())
