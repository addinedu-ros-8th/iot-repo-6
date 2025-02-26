import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from adminUserinfoDetail import adminUserinfoDetailWindow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))     # 현재 스크립트의 부모 디렉터리를 sys.path에 추가
from controller.database.database_manager import DB

form_class = uic.loadUiType("adminUserinfo.ui")[0]

class adminUserinfoWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("admin User info")

        self.detailButton.clicked.connect(self.detailShow)
        self.exitButton.clicked.connect(self.exitShow)
        self.backButton.clicked.connect(self.backShow)

        self.loadData()

    def detailShow(self):
        print("detail show")
        self.close()
        self.main_window = adminUserinfoDetailWindow()
        self.main_window.show()


    def backShow(self):
        from adminMain import adminMainWindow  
        self.close()
        self.main_window = adminMainWindow()
        self.main_window.show()

    def exitShow(self):
        self.close()
    
    def loadData(self):
        try:
            db = DB(db_name="iot")
            db.connect()
            db.set_cursor_buffered_true()

            # 🔹 테이블의 컬럼명 가져오기
            db.execute("SHOW COLUMNS FROM user")
            column_names = [row[0] for row in db.fetchall()]  # 첫 번째 값이 컬럼명

            # 🔹 데이터 가져오기
            db.execute("SELECT * FROM user")
            rows = db.fetchall()
            # user_num, user_id, user_password, user_card_id, farm_kit_id, phone_number, name
            if not rows:
                QMessageBox.information(self, "정보", "데이터가 없습니다.")
                return

            self.tableWidget.setRowCount(len(rows))  # 행 개수 설정
            self.tableWidget.setColumnCount(len(column_names))  # 열 개수 설정
            self.tableWidget.setHorizontalHeaderLabels(column_names)  # 컬럼명 설정

            # 🔹 데이터 삽입
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            db.close()

        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 불러오기 실패: {str(e)}")