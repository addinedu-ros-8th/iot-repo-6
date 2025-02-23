from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys
# from userKitRentalDetail import userRegisterWindow

form_class = uic.loadUiType("userPlantDetail.ui")[0]

class plantInfoWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("user plant Detial")
        self.closeButton.clicked.connect(self.closeClicked)

    def closeClicked(self):
        sys.exit()