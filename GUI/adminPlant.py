from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from adminPlantDetail import adminPlantDetailWindow

form_class = uic.loadUiType("adminPlant.ui")[0]

class adminPlantWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("admin Plant")

        self.detailButton.clicked.connect(self.detailShow)
    
    def detailShow(self):
        print("detail show")
        self.close()
        self.main_window = adminPlantDetailWindow()
        self.main_window.show()
