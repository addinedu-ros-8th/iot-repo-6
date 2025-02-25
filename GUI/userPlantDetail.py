from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.database.database_manager import DB
# from userKitRentalDetail import userRegisterWindow

form_class = uic.loadUiType("userPlantDetail.ui")[0]

class plantInfoWindow(QMainWindow, form_class):
    def __init__(self,user_num):
        super().__init__()
        self.setupUi(self)

        self.user_num = user_num

        self.userName.setText(str(self.user_num))

        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()

        self.setWindowTitle("user plant Detial")
        self.closeButton.clicked.connect(self.closeClicked)

    def closeClicked(self):
        sys.exit()