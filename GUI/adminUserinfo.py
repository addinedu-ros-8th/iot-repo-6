from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from adminUserinfoDetail import adminUserinfoDetailWindow

form_class = uic.loadUiType("adminUserinfo.ui")[0]

class adminUserinfoWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("admin User info")

        self.detailButton.clicked.connect(self.detailShow)
    
    def detailShow(self):
        print("detail show")
        self.close()
        self.main_window = adminUserinfoDetailWindow()
        self.main_window.show()