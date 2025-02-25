import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))     # 현재 스크립트의 부모 디렉터리를 sys.path에 추가
from backend.database.database_manager import DB

form_class = uic.loadUiType("adminUserinfoDetail.ui")[0]

class adminUserinfoDetailWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("admin User info Detail")

        self.cancelButton.clicked.connect(self.cancelShow)
        self.pw_resetButton.clicked.connect(self.pwresetShow)
        self.okButton.clicked.connect(self.okShow)

        self.loadData()
        self.nameData()

    # def okShow(self):
    #     try:
    #         selected_user_id = self.comboBox_2.currentText()  # 선택된 user_id 가져오기
    #         selected_card_id = self.comboBox.currentText()

    #         if not selected_user_id:
    #             QMessageBox.warning(self, "경고", "변경할 사용자를 선택하세요.")
    #             return
            
    #         print(f"선택된 user_id: {selected_user_id}")  # 디버깅 로그
    #         print(f"선택된 user_card_id: {selected_card_id}")  # 디버깅 로그

    #         db = DB(db_name="iot")
    #         db.connect()
    #         db.set_cursor_buffered_true()

    #         query = "UPDATE user SET user_card_id = %s WHERE user_id = %s"
    #         db.execute(query, (int(selected_card_id), int(selected_user_id)))
            
    #         db.close()
    #         self.close()
    #         print("change success")

    #     except Exception as e:
    #         QMessageBox.critical(self, "오류", f"데이터 불러오기 실패: {str(e)}")
    def okShow(self):
        try:
            selected_user_id = self.comboBox_2.currentText()  # 선택된 user_id 가져오기
            selected_card_id = self.comboBox.currentText()  # 선택된 user_card_id 가져오기

            if not selected_user_id or not selected_card_id:
                QMessageBox.warning(self, "경고", "변경할 사용자와 카드를 선택하세요.")
                return
            
            print(f"선택된 user_id: {selected_user_id}")  
            print(f"선택된 user_card_id: {selected_card_id}")  
            
            db = DB(db_name="iot")
            db.connect()
            db.set_cursor_buffered_true()

            query = "SELECT user_num FROM user WHERE user_id = %s"
            db.execute(query, (selected_user_id,))
            result = db.fetchone()

            if not result:
                QMessageBox.warning(self, "오류", "해당 user_id가 존재하지 않습니다.")
                return
            
            user_num = result[0]  # user_num 가져오기
            print(f"조회된 user_num: {user_num}")  # 디버깅 로그

            query = "UPDATE user SET user_card_id = %s WHERE user_num = %s"
            db.execute(query, (int(selected_card_id), int(user_num)))

            db.commit()  
            print("데이터베이스 업데이트 완료") 
            QMessageBox.information(self, "완료", "카드 정보가 변경되었습니다.")

            db.close()

        except Exception as e:
            QMessageBox.critical(self, "오류", f"카드 정보 변경 실패: {str(e)}")

    def pwresetShow(self):
        try:
            selected_user_id = self.comboBox_2.currentText()  # 선택된 user_id 가져오기
            if not selected_user_id:
                QMessageBox.warning(self, "경고", "변경할 사용자를 선택하세요.")
                return
            db = DB(db_name="iot")
            db.connect()
            db.set_cursor_buffered_true()

            query = "UPDATE user SET user_password = %s WHERE user_id = %s"
            db.execute(query, ('0000', selected_user_id))

            db.commit()
            QMessageBox.information(self, "완료", "비밀번호가 '0000'으로 초기화되었습니다.")

            db.close()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 불러오기 실패: {str(e)}")

    
    def cancelShow(self):
        from adminUserinfo import adminUserinfoWindow  
        self.close()
        self.main_window = adminUserinfoWindow()
        self.main_window.show()

    def nameData(self):
        try:
            db = DB(db_name="iot")
            db.connect()
            db.set_cursor_buffered_true()

            db.execute("SELECT user_id FROM user")
            data = db.fetchall()

            self.comboBox_2.clear()


            for row in data:
                self.comboBox_2.addItem(str(row[0]))  # QComboBox에 데이터 추가

            db.close()

            self.comboBox_2.currentIndexChanged.connect(self.updateUserName)
        
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 불러오기 실패: {str(e)}")

    def updateUserName(self):
        try:
            selected_card = self.comboBox_2.currentText()  # 선택된 user_card 값
            if not selected_card:
                self.textEdit.clear()
                return
            db = DB(db_name="iot")
            db.connect()
            db.set_cursor_buffered_true()
            
            query = "SELECT name FROM user WHERE user_id = %s"
            db.execute(query, (selected_card,))
            result = db.fetchone()

            print(f"DB 조회 결과: {result}")  # 디버깅 로그
            if result:
                self.textEdit.setText(result[0])  # 사용자 이름 출력
            else:
                self.textEdit.clear()

                db.close()

        except Exception as e:
            QMessageBox.critical(self, "오류", f"사용자 정보 불러오기 실패: {str(e)}")           

    def loadData(self):
        try:
            db = DB(db_name="iot")
            db.connect()
            db.set_cursor_buffered_true()

            db.execute("SELECT user_card_id FROM user_card")
            data = db.fetchall()

            self.comboBox.clear()

            for row in data:
                self.comboBox.addItem(str(row[0]))  # QComboBox에 데이터 추가

            db.close()
        
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 불러오기 실패: {str(e)}")