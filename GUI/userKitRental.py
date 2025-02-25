from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from backend.database.database_manager import DB

form_class = uic.loadUiType("userKitRental.ui")[0]

class kitRentWindow(QMainWindow, form_class):

    def __init__(self, user_num):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Kit Rental")
        
        self.user_num = user_num

        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()

        # self.kitRentButton.clicked.connect(self.save_rental_kit)
        self.okBtn.clicked.connect(self.kitRentShow)

        
        # self.update_labels()

    def kitRentShow(self):
        print("Kit rent")
        self.close()
        
        from userRegister import userRegisterWindow 
        self.main_window = userRegisterWindow(self.user_num)
        self.main_window.show()