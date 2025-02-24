from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("adminPlant.ui")[0]

class adminPlantWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("admin Plant")

        self.backButton.clicked.connect(self.backShow)
        self.exitButton.clicked.connect(self.exitShow)

    def exitShow(self):
        self.close()

    def backShow(self):
        from adminMain import adminMainWindow  
        self.close()
        self.main_window = adminMainWindow()
        self.main_window.show()
