import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime
from PyQt5 import uic
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from controller.database.database_manager import DB
# from userRegister import userRegisterWindow
# from userKitRentalDetail import userRegisterWindow

form_class = uic.loadUiType("userPlantDetail.ui")[0]

class userPlantDetailWindow(QMainWindow, form_class):
    def __init__(self, user_num):
        super().__init__()
        self.setupUi(self)
        self.user_num = user_num
        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()

        self.kitNum.setText("농장 번호: ")
        self.get_farm_num()  
        self.get_plant_name() 
        self.get_planting_days()  
        self.update_air_temperature()  
        self.update_air_moisture()  
        self.update_soil_moisture()
        self.update_light_intensity()
        self.update_plant_type()  
        self.update_rental_startdate()

        self.setWindowTitle("user plant Detail")
        self.closeButton.clicked.connect(self.closeClicked)

        self.num_box.currentIndexChanged.connect(self.on_farm_selected)
        
        # 카메라 설정
        self.cap = cv2.VideoCapture(0)  # 기본 카메라 사용 (0번)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms마다 프레임 업데이트

    def update_frame(self):
        """카메라 프레임을 받아와 QLabel에 표시"""
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR -> RGB 변환
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.camera_label.setPixmap(QPixmap.fromImage(qimg))

    def closeClicked(self):
        self.cap.release()  # 카메라 해제
        sys.exit()

    def get_farm_num(self):
        query = """SELECT farm_kit_id 
               FROM rental_kit 
               WHERE user_id = %s"""
    
        self.db.cursor.execute(query, (self.user_num,))
        farm_kit_ids = self.db.cursor.fetchall()
        
        self.num_box.clear()

        for farm_kit_id in farm_kit_ids:
            query_farm_num = """SELECT farm_num 
                                FROM farm_kit 
                                WHERE farm_kit_id = %s"""
            
            self.db.cursor.execute(query_farm_num, (farm_kit_id[0],))
            farm_num = self.db.cursor.fetchone()
            
            if farm_num:
                self.num_box.addItem(f"농장 번호: {farm_num[0]}", farm_kit_id[0])

    def on_farm_selected(self):
        """콤보박스에서 농장 번호를 선택하면 해당 농장의 데이터를 갱신"""
        selected_farm_kit_id = self.num_box.currentData() 

        if selected_farm_kit_id is None:
            return
        
        self.clear_labels()

        self.get_plant_name(selected_farm_kit_id)
        self.get_planting_days(selected_farm_kit_id)
        self.update_air_temperature(selected_farm_kit_id)
        self.update_air_moisture(selected_farm_kit_id)
        self.update_soil_moisture(selected_farm_kit_id)
        self.update_light_intensity(selected_farm_kit_id)
        self.update_plant_type(selected_farm_kit_id)
        self.update_rental_startdate(selected_farm_kit_id)

    def clear_labels(self):
        """기존 데이터를 초기화"""
        self.label_2.setText("식물 닉네임: ")
        self.label_8.setText("식물 심은 날짜: ")
        self.label_3.setText("공기 온도: ")
        self.label_4.setText("공기 습도: ")
        self.label_9.setText("흙 습도: ")
        self.label_5.setText("광도: ")
        self.label_6.setText("식물 종류: ")
        self.label_7.setText("시작일: ")

    def get_plant_name(self, farm_kit_id=None):
        sql = """select plant_nickname
                 from rental_kit
                 WHERE user_id = %s"""
        if farm_kit_id:
            sql += " AND farm_kit_id = %s"
            self.db.cursor.execute(sql, (self.user_num, farm_kit_id))
        else:
            self.db.cursor.execute(sql, (self.user_num,))
        plant_nickname = self.db.cursor.fetchone()
        self.label_2.setText(f"식물 닉네임: {plant_nickname[0]}")

    def get_planting_days(self, farm_kit_id=None):
        sql = """SELECT r.planting_date
                 FROM rental_kit r
                 WHERE r.user_id = %s"""
        if farm_kit_id:
            sql += " AND r.farm_kit_id = %s"
            self.db.cursor.execute(sql, (self.user_num, farm_kit_id))
        else:
            self.db.cursor.execute(sql, (self.user_num,))
        
        planting_date = self.db.cursor.fetchone()

        planting_date = planting_date[0]
        current_date = datetime.now()
        days_since_planting = (current_date - planting_date).days
        self.label_8.setText(f"--{days_since_planting}일째!")

    def update_air_temperature(self, farm_kit_id=None):
        query = """SELECT ps.temperature
                    FROM rental_kit rk
                    JOIN plant_status ps ON rk.farm_kit_id = ps.farm_kit_id
                    WHERE rk.user_id = %s"""
        if farm_kit_id:
            query += " AND rk.farm_kit_id = %s"
            self.db.cursor.execute(query, (self.user_num, farm_kit_id))
        else:
            self.db.cursor.execute(query, (self.user_num,))

        air_temperature = self.db.cursor.fetchone()
        self.label_3.setText(f"공기 온도: {air_temperature[0]}°C")

    def update_air_moisture(self, farm_kit_id=None):
        query = """SELECT ps.humidity
                    FROM rental_kit rk
                    JOIN plant_status ps ON rk.farm_kit_id = ps.farm_kit_id
                    WHERE rk.user_id = %s"""
        if farm_kit_id:
            query += " AND rk.farm_kit_id = %s"
            self.db.cursor.execute(query, (self.user_num, farm_kit_id))
        else:
            self.db.cursor.execute(query, (self.user_num,))

        air_moisture = self.db.cursor.fetchone()
        self.label_4.setText(f"공기 습도: {air_moisture[0]}%")

    def update_soil_moisture(self, farm_kit_id=None):
        query = """SELECT ps.soil_moisture
                    FROM rental_kit rk
                    JOIN plant_status ps ON rk.farm_kit_id = ps.farm_kit_id
                    WHERE rk.user_id = %s"""
        if farm_kit_id:
            query += " AND rk.farm_kit_id = %s"
            self.db.cursor.execute(query, (self.user_num, farm_kit_id))
        else:
            self.db.cursor.execute(query, (self.user_num,))

        soil_moisture = self.db.cursor.fetchone()
        self.label_9.setText(f"흙 습도: {soil_moisture[0]}%")

    def update_light_intensity(self, farm_kit_id=None):
        query = """SELECT ps.light_intensity
                    FROM rental_kit rk
                    JOIN plant_status ps ON rk.farm_kit_id = ps.farm_kit_id
                    WHERE rk.user_id = %s"""
        if farm_kit_id:
            query += " AND rk.farm_kit_id = %s"
            self.db.cursor.execute(query, (self.user_num, farm_kit_id))
        else:
            self.db.cursor.execute(query, (self.user_num,))

        light_intensity = self.db.cursor.fetchone()
        self.label_5.setText(f"광도: {light_intensity[0]}cd")

    def update_plant_type(self, farm_kit_id=None):
        query = """SELECT p.plant_name 
                FROM rental_kit r
                JOIN plant p ON r.plant_id = p.plant_id
                WHERE r.user_id = %s"""
        if farm_kit_id:
            query += " AND r.farm_kit_id = %s"
            self.db.cursor.execute(query, (self.user_num, farm_kit_id))
        else:
            self.db.cursor.execute(query, (self.user_num,))

        plant_name = self.db.cursor.fetchone()
        self.label_6.setText(f"식물 종류: {plant_name[0]}")

    def update_rental_startdate(self, farm_kit_id=None):
        query = """SELECT rental_startdate 
                FROM rental_kit 
                WHERE rental_kit_id = %s"""
        if farm_kit_id:
            query += " AND farm_kit_id = %s"
            self.db.cursor.execute(query, (self.user_num, farm_kit_id))
        else:
            self.db.cursor.execute(query, (self.user_num,))

        rental_startdate = self.db.cursor.fetchone()
        if rental_startdate is None:
            self.label_7.setText("시작일: 정보 없음")
        else:
            self.label_7.setText(f"시작일: {rental_startdate[0]}")

    def closeClicked(self):
        sys.exit()