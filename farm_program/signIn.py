import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from signUp import signUpWindow
from userRegister import userRegisterWindow
from adminMain import adminMainWindow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))     # 현재 스크립트의 부모 디렉터리를 sys.path에 추가
from backend.database.database_manager import DB

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
        username = self.usernameTedit.toPlainText().strip()
        password = self.passwordTedit.toPlainText().strip()
    
        db = DB(db_name="iot")
        db.connect()
        db.set_cursor_buffered_true()
        db.execute("SELECT user_num FROM user WHERE user_id = %s AND user_password = %s", (username, password))
        result = db.fetchall()

        if username == "admin" and password == "1234":
            print("Admin login success")
            self.close()
            self.main_window = adminMainWindow()
            self.main_window.show()

        elif result and result[0][0] > 0:
            print("User login success")
            user_num = result[0][0]
            print(user_num)
            self.close()
            self.main_window = userRegisterWindow(user_num)
            self.main_window.show()
            
        else:
            QMessageBox.warning(self, "로그인 오류", "아이디 또는 비밀번호가 틀렸습니다.")
            
    def signUp(self):
        print("Sign up")
        self.main_window = signUpWindow()
        self.main_window.show()