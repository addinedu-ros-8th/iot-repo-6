from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from userPlantDetail import plantInfoWindow
from backend.database.database_manager import DB

form_class = uic.loadUiType("userKitRentalDetail.ui")[0]

class userKitRentalDetailWindow(QMainWindow, form_class):

    db = DB(db_name="iot")
    db.connect()
    db.set_cursor_buffered_true()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Kit Rental Detail")

        self.load_plant_names()

        self.selectButton.clicked.connect(self.kitRentShow)

    

    
    def kitRentShow(self):
        print("Kit rent detail")
        self.close()
        self.main_window = plantInfoWindow()
        self.main_window.show()

    def load_plant_names(self):
        query = "SELECT plant_name FROM plant;" 
        result = self.db.fetch_all(query)  
        
        self.typeCombo.clear()
        for row in result:
            self.typeCombo.addItem(row[0])