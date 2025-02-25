import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from GUI.userPlantRegist import userPlantRegistWindow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.database.database_manager import DB
from userPlantDetail import userPlantDetailWindow

form_class = uic.loadUiType("userRegister.ui")[0]

class userRegisterWindow(QMainWindow, form_class):
    def __init__(self, user_num):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("User Register")

        self.user_num = user_num

        self.userName.setText(str(self.user_num))
        self.kitRentButton.clicked.connect(self.kitRentShow)
        self.plantInfoButton.clicked.connect(self.plantInfoShow)
    
    def kitRentShow(self):
        print("Kit rent")
        self.close()

        from userKitRental import kitRentWindow  
        self.main_window = kitRentWindow(self.user_num)
        self.main_window.show()

    def plantInfoShow(self):
        print("Plant info")
        
        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()

        query_check_farm_kit = "SELECT farm_kit_id FROM rental_kit WHERE user_id = %s"
        self.db.cursor.execute(query_check_farm_kit, (self.user_num,))
        rental_kit = self.db.cursor.fetchone()

        if not rental_kit or rental_kit[0] is None:  # farm_kit_id가 없다면
            print(f"user_id {self.user_num}의 rental_kit에 farm_kit_id가 없음 → 등록 페이지로 이동")
            QMessageBox.warning(self, "경고", "등록된 농장 키트가 없습니다.")
            return  # 경고창을 띄운 후, 함수 종료로 창 변경을 막습니다.
        
        query = "SELECT plant_id FROM rental_kit WHERE user_id = %s"
        self.db.execute(query, (self.user_num,))
        result = self.db.fetchone()

        if result and result[0] is not None: 
            print(f"user_id {self.user_num}의 plant_id가 rental_kit 테이블에 존재 → Kit Rental Detail 페이지로 이동")
            self.main_window = userPlantDetailWindow(self.user_num)
        else:  
            print(f"user_id {self.user_num}의 plant_id가 없음 → Plant Info 페이지로 이동")
            self.main_window = userPlantRegistWindow(self.user_num)

        self.close()  # 현재 창 닫기
        self.main_window.show()  # 새 창 열기
