from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from backend.database.database_manager import DB

form_class = uic.loadUiType("userKitRental.ui")[0]

class kitRentWindow(QMainWindow, form_class):

    db = DB(db_name="iot")
    db.connect()
    db.set_cursor_buffered_true()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Kit Rental")

        self.kitRentButton.clicked.connect(self.kitRentShow)
    
    def kitRentShow(self):
        print("Kit rent")
        self.close()
        
        from userRegister import userRegisterWindow 
        self.main_window = userRegisterWindow()
        self.main_window.show()
