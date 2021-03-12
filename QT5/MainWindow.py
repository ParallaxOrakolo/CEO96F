from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDialog,
    QApplication,
    QAction
)

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from JsonMod import JsonMod
from random import randint
from PyQt5 import QtCore

import numpy as np
import json
import sys
import cv2
import os

jsonpath = "json-data.json"
cap = False
marker_s = False

photoPath = os.path.normpath(os.path.join(os.path.dirname(__file__), '../Images/Foto.jpg'))


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0, 100))
        layout.addWidget(self.label)
        self.setLayout(layout)


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
            img = cv2.imread('../Images/block.png')
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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Ui/mainWindow.ui", self)
        self.window1 = JsonTree()
        self.window2 = MachineController()

        self.actionSair.triggered.connect(self.quit_trigger)
        self.actionJson_Editor.triggered.connect(lambda checked: self.toggle_window(self.window1))
        self.actionMachine.triggered.connect(lambda checked: self.toggle_window(self.window2))
        self.actionCam.triggered.connect(lambda checked: self.toggle_window(self.window3))

    def quit_trigger(self):
        sys.exit(200)


    def toggle_window(self, window):
        if window.isVisible():
            window.hide()

        else:
            if window.windowTitle() == self.window2.windowTitle():
                window.showFullScreen()
            else:
                window.show()


app = QApplication(sys.argv)
view = JsonMod.QtWidgets.QTreeView()
model = JsonMod.QJsonModel()

with open(jsonpath) as f:
    model.load(json.load(f))

view.setModel(model)

w = MainWindow()
w.show()
sys.exit(app.exec_())
