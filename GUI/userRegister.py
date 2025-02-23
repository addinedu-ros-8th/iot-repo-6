from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from userKitRental import kitRentWindow
from userPlantDetail import plantInfoWindow

form_class = uic.loadUiType("userRegister.ui")[0]

class userRegisterWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("User Resgister")

        self.kitRentButton.clicked.connect(self.kitRentShow)
        self.plantInfoButton.clicked.connect(self.plantInfoShow)
    
    def kitRentShow(self):
        print("Kit rent")
        self.close()
        self.main_window = kitRentWindow()
        self.main_window.show()

    def plantInfoShow(self):
        print("Plant info")
        self.close()
        self.main_window = plantInfoWindow()
        self.main_window.show()


