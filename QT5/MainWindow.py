from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt5.uic import loadUi
from JsonMod import JsonMod
from random import randint
import json
import sys

jsonpath = "json-data.json"


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


class JsonTree(QWidget):

    def __init__(self):
        super(JsonTree, self).__init__()
        loadUi("jsonViwer.ui", self)
        self.savebtw.clicked.connect(self.saveData)
        self.TrewView()

    def TrewView(self):
        view.setColumnWidth(0, int(self.label.width()/2))
        self.vt.addWidget(view)
    
    def saveData(self)
        bkp = model.json()
        with open(jsonpath, 'w', encoding='utf-8') as jsonFile2:
            json.dump(bkp, jsonFile2, indent=4)





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window1 = AnotherWindow()
        self.window2 = JsonTree()

        l = QVBoxLayout()
        button1 = QPushButton("Push for Window 1")
        button1.clicked.connect(
            lambda checked: self.toggle_window(self.window1)
        )
        l.addWidget(button1)

        button2 = QPushButton("Push for Window 2")
        button2.clicked.connect(
            lambda checked: self.toggle_window(self.window2)
        )
        l.addWidget(button2)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def toggle_window(self, window):
        if window.isVisible():
            window.hide()

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
app.exec_()
