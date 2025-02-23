from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
# from userKitRental import kitRentWindow

form_class = uic.loadUiType("userKitRentalDetail.ui")[0]

class userRegisterWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Kit Rental Detail")

    #     self.kitRentButton.clicked.connect(self.kitRentShow)
    
    # def kitRentShow(self):
    #     print("Kit rent detail")
    #     self.close()
    #     self.main_window = kitRentWindow()
    #     self.main_window.show()
