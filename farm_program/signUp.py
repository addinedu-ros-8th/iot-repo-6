import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))     # 현재 스크립트의 부모 디렉터리를 sys.path에 추가
from controller.database.database_manager import DB

current_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(current_dir)
form_class = uic.loadUiType("signUp.ui")[0]

class signUpWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Sign up")

        self.signUpButton.clicked.connect(self.signUpButtonClicked)

    def signUpButtonClicked(self):
        First_name = self.firstNameTedit.toPlainText().strip()
        Last_name = self.lastNameTedit.toPlainText().strip()
        Username = self.userNameTedit.toPlainText().strip()
        Phone_number = self.phoneNumberTedit.toPlainText().strip()
        Password = self.passwordTedit.toPlainText().strip()
        Confirm_password = self.confirmPasswordTedit.toPlainText().strip()

        if not (First_name and Last_name and Username and Phone_number and Password and Confirm_password):
            QMessageBox.warning(self, "입력 오류", "모든 필드를 입력해주세요.")
            return

        if Password != Confirm_password:
            QMessageBox.warning(self, "비밀번호 오류", "비밀번호가 일치하지 않습니다.")
            return

        full_name = f"{First_name}{Last_name}"

        db = DB(db_name="iot")
        db.connect()
        db.set_cursor_buffered_true()

        # 중복된 user_id 확인
        db.execute("SELECT COUNT(*) FROM user WHERE user_id = %s", (Username,))
        if db.fetchone()[0] > 0:
            QMessageBox.warning(self, "회원가입 오류", "이미 존재하는 사용자 이름입니다.")
            return

        # 데이터 삽입
        try:
            db.execute("""
                INSERT INTO user (user_id, user_password, phone_number, name)
                VALUES (%s, %s, %s, %s)
            """, (Username, Password, Phone_number, full_name))
            db.commit()
            
            db.execute("""
                INSERT INTO rental_kit (user_id)
                VALUES (%s)
            """, (Username,))
            db.commit()

            QMessageBox.information(self, "회원가입 성공", "회원가입이 완료되었습니다!")
            self.close()
        except Exception as e:
            db.rollback()
            QMessageBox.critical(self, "데이터베이스 오류", f"회원가입 중 오류 발생: {str(e)}")
        finally:
            db.close()

