from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from userKitRentalDetail import userRegisterWindow

form_class = uic.loadUiType("userKitRental.ui")[0]

class kitRentWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Kit Rental")

        self.kitRentButton.clicked.connect(self.kitRentShow)
    
    def kitRentShow(self):
        print("Kit rent")
        self.close()
        self.main_window = userRegisterWindow()
        self.main_window.show()
