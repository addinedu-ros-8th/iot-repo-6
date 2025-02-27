import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from userPlantRegist import userPlantRegistWindow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from controller.database.database_manager import DB
from userPlantDetail import userPlantDetailWindow
from userKitRental import kitRentWindow  

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
        self.main_window = kitRentWindow(self.user_num)
        self.main_window.show()

    def plantInfoShow(self):
        print("Plant info")
        
        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()

        # 유저가 대여한 모든 farm_kit_id 가져오기
        query_check_farm_kit = "SELECT farm_kit_id FROM rental_kit WHERE user_id = %s"
        self.db.execute(query_check_farm_kit, (self.user_num,))
        rental_kits = self.db.fetchall()  # 여러 개의 키트 가능

        if not rental_kits:  # 대여한 키트가 없을 경우
            print(f"user_id {self.user_num}의 rental_kit에 farm_kit_id가 없음 → 등록 페이지로 이동")
            QMessageBox.warning(self, "경고", "등록된 농장 키트가 없습니다.")
            return  # 창 변경을 막음

        # rental_kit 테이블에서 유저의 모든 대여 기록 확인
        query = "SELECT rental_kit_id, plant_id FROM rental_kit WHERE user_id = %s"
        self.db.execute(query, (self.user_num,))
        rentals = self.db.fetchall()  # 여러 개의 키트 대여 가능

        if not rentals:
            print(f"user_id {self.user_num}가 rental_kit 테이블에 없음 → Kit Rental Detail 페이지로 이동")
            self.main_window = kitRentWindow(self.user_num)
        else:
            # 등록되지 않은 식물이 있는지 확인 (plant_id가 NULL 또는 None이면 등록이 안 됨)
            unregistered_kits = [rental for rental in rentals if rental[1] is None]

            if unregistered_kits:
                print(f"user_id {self.user_num}가 대여한 키트 중 식물이 등록되지 않은 키트 발견 → 식물 등록 페이지로 이동")
                self.main_window = userPlantRegistWindow(self.user_num)  # 식물 등록 UI로 이동
            else:
                print(f"user_id {self.user_num}의 모든 키트가 식물 등록 완료 → Plant Info 페이지로 이동")
                self.main_window = userPlantDetailWindow(self.user_num)  # 식물 정보 UI로 이동

        self.close()  # 현재 창 닫기
        self.main_window.show()  # 새 창 열기