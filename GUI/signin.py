import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from signUp import signUpWindow
from userRegister import userRegisterWindow

current_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_dir)
form_class = uic.loadUiType("signIn.ui")[0]

class SignInWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Sign in")

        self.signupButton.clicked.connect(self.signUp)
        self.signinButton.clicked.connect(self.userMain)
    
    def userMain(self):
        print("Sign in success")
        
        self.close()
        self.main_window = userRegisterWindow()
        self.main_window.show()
    
    def signUp(self):
        print("Sign up")
        self.main_window = signUpWindow()
        self.main_window.show()

    