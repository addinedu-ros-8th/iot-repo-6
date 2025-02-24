from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from userPlantDetail import plantInfoWindow

form_class = uic.loadUiType("userKitRentalDetail.ui")[0]

class userKitRentalDetailWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Kit Rental Detail")

        self.selectButton.clicked.connect(self.kitRentShow)
    
    def kitRentShow(self):
        print("Kit rent detail")
        self.close()
        self.main_window = plantInfoWindow()
        self.main_window.show()
