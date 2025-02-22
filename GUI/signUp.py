from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("signup.ui")[0]

class signUpWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Sign up")

        self.signUpButton.clicked.connect(self.signUpButtonClicked)

    def signUpButtonClicked(self):
        # show success alter
        self.close()

