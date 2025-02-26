from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from adminUserinfo import adminUserinfoWindow
from adminKit import adminKitWindow
from adminPlant import adminPlantWindow

form_class = uic.loadUiType("adminMain.ui")[0]

class adminMainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("admin Main")

        self.userinfoButton.clicked.connect(self.userinfoShow)
        self.kitinfoButton.clicked.connect(self.kitinfoShow)
        self.plantinfoButton.clicked.connect(self.plantinfoShow)

    def userinfoShow(self):
        print("admin user info")
        self.close()
        self.main_window = adminUserinfoWindow()
        self.main_window.show()

    def kitinfoShow(self):
        print("admin kit")
        self.close()
        self.main_window = adminKitWindow()
        self.main_window.show()

    def plantinfoShow(self):
        print("admin plant")
        self.close()
        self.main_window = adminPlantWindow()
        self.main_window.show()