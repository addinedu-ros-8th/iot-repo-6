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

    def __init__(self,user_id):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Kit Rental Detail")

        self.user_id = user_id

        self.load_plant_names()

        self.selectButton.clicked.connect(self.kitRentShow)

    

    
    def kitRentShow(self):
        print("Kit rent detail")
        self.close()
        self.main_window = plantInfoWindow()
        self.main_window.show()

    def load_plant_names(self):
        query = "SELECT plant_name FROM plant;"
        self.db.execute(query)
        result = self.db.fetchall()  
        
        self.typeCombo.clear()
        for row in result:
            self.typeCombo.addItem(row[0])