from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("adminKit.ui")[0]

class adminKitWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("admin Kit")

        self.exitButton.clicked.connect(self.exitShow)

    def exitShow(self):
        print("exit show")
        self.close()