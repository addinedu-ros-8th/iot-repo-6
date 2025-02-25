import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from userKitRentalDetail import userKitRentalDetailWindow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.database.database_manager import DB
from userPlantDetail import plantInfoWindow

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

        # rental_kit 테이블에서 user_id가 self.user_num과 일치하는지 확인
        query = "SELECT user_id FROM rental_kit WHERE user_id = %s"
        self.db.execute(query, (self.user_num,))
        result = self.db.fetchone()

        if result and result[0] == self.user_num:  # user_id 값이 정확히 일치하면 plantInfoWindow로 이동
            print(f"user_id {self.user_num}가 rental_kit 테이블에 존재 → Plant Info 페이지로 이동")
            self.main_window = plantInfoWindow(self.user_num)  
        else:  # 존재하지 않으면 Kit Rental Detail 페이지로 이동
            print(f"user_id {self.user_num}가 rental_kit 테이블에 없음 → Kit Rental Detail 페이지로 이동")
            self.main_window = userKitRentalDetailWindow(self.user_num)

        self.close()  # 현재 창 닫기
        self.main_window.show()  # 새 창 열기
