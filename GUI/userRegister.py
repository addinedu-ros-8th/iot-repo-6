from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from userKitRentalDetail import userKitRentalDetailWindow

form_class = uic.loadUiType("userRegister.ui")[0]

class userRegisterWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("User Register")

        self.kitRentButton.clicked.connect(self.kitRentShow)
        self.plantInfoButton.clicked.connect(self.plantInfoShow)
    
    def kitRentShow(self):
        print("Kit rent")
        self.close()

        from userKitRental import kitRentWindow  
        self.main_window = kitRentWindow()
        self.main_window.show()

    def plantInfoShow(self):
        print("Plant info")
        self.close()
        self.main_window = userKitRentalDetailWindow()
        self.main_window.show()
