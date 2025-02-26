from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime
from PyQt5 import uic
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.database.database_manager import DB
# from userRegister import userRegisterWindow
# from userKitRentalDetail import userRegisterWindow

form_class = uic.loadUiType("userPlantDetail.ui")[0]

class userPlantDetailWindow(QMainWindow, form_class):
    def __init__(self,user_num):
        super().__init__()
        self.setupUi(self)
        self.user_num = user_num
        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()

        self.get_farm_num()
        self.get_plant_name()
        self.get_planting_days()
        self.update_air_temperature()
        self.update_air_moisture()
        self.update_soil_moisture()
        self.update_light_intensity()
        self.update_plant_type()
        self.update_rental_startdate()

        self.setWindowTitle("user plant Detial")
        self.closeButton.clicked.connect(self.closeClicked)

    def get_farm_num(self):
        query = """SELECT farm_kit_id 
                   FROM rental_kit 
                   WHERE user_id = %s"""
        
        self.db.cursor.execute(query, (self.user_num,))
        farm_kit_id = self.db.cursor.fetchone()
        
        query_farm_num = """SELECT farm_num 
                            FROM farm_kit 
                            WHERE farm_kit_id = %s"""
        
        self.db.cursor.execute(query_farm_num, (farm_kit_id[0],))
        farm_num = self.db.cursor.fetchone()
        self.kitNum.setText(f"농장 번호: {farm_num[0]}")

    def get_plant_name(self):
        sql = """select plant_nickname
                 from rental_kit
                 WHERE user_id = %s"""
        self.db.cursor.execute(sql, (self.user_num,))
        plant_nickname = self.db.cursor.fetchone()
        self.label_2.setText(f"식물 닉네임: {plant_nickname[0]}")

    def get_planting_days(self):
        sql = """SELECT r.planting_date
                 FROM rental_kit r
                 WHERE r.user_id = %s"""
        
        self.db.cursor.execute(sql, (self.user_num,))
        planting_date = self.db.cursor.fetchone()

        planting_date = planting_date[0]
        current_date = datetime.now()
        days_since_planting = (current_date - planting_date).days
        self.label_8.setText(f"--{days_since_planting}일째!")

    def update_air_temperature(self):
        query = """SELECT ps.temperature
                    FROM rental_kit rk
                    JOIN plant_status ps ON rk.farm_kit_id = ps.farm_kit_id
                    WHERE rk.user_id = %s
                    ORDER BY ps.timestamp DESC
                    LIMIT 1;"""
        
        self.db.cursor.execute(query, (self.user_num,))
        air_temperature = self.db.cursor.fetchone()


        self.label_3.setText(f"공기 온도: {air_temperature[0]}°C")


    def update_air_moisture(self):
        query = """SELECT ps.humidity
                    FROM rental_kit rk
                    JOIN plant_status ps ON rk.farm_kit_id = ps.farm_kit_id
                    WHERE rk.user_id = %s
                    ORDER BY ps.timestamp DESC
                    LIMIT 1;"""
        
        self.db.cursor.execute(query, (self.user_num,))
        air_moisture = self.db.cursor.fetchone()

        self.label_4.setText(f"공기 습도: {air_moisture[0]}%")

    def update_soil_moisture(self):
        query = """SELECT ps.soil_moisture
                    FROM rental_kit rk
                    JOIN plant_status ps ON rk.farm_kit_id = ps.farm_kit_id
                    WHERE rk.user_id = %s
                    ORDER BY ps.timestamp DESC
                    LIMIT 1;"""
        
        self.db.cursor.execute(query, (self.user_num,))
        soil_moisture = self.db.cursor.fetchone()

        self.label_9.setText(f"흙 습도: {soil_moisture[0]}%")


    def update_light_intensity(self):
        query = """SELECT ps.light_intensity
                    FROM rental_kit rk
                    JOIN plant_status ps ON rk.farm_kit_id = ps.farm_kit_id
                    WHERE rk.user_id = %s
                    ORDER BY ps.timestamp DESC
                    LIMIT 1;"""
        
        self.db.cursor.execute(query, (self.user_num,))
        light_intensity = self.db.cursor.fetchone()

        self.label_3.setText(f"광도: {light_intensity[0]}cd")

    def update_plant_type(self):
        query = """SELECT p.plant_name 
                FROM rental_kit r
                JOIN plant p ON r.plant_id = p.plant_id
                WHERE r.user_id = %s"""
        
        self.db.cursor.execute(query, (self.user_num,))
        plant_name = self.db.cursor.fetchone()

        self.label_6.setText(f"식물 종류: {plant_name[0]}")

    def update_rental_startdate(self):
        query = """SELECT rental_startdate 
                FROM rental_kit 
                WHERE rental_kit_id = %s"""

        self.db.cursor.execute(query, (self.user_num,))
        rental_startdate = self.db.cursor.fetchone()

        self.label_7.setText(f"시작일: {rental_startdate[0]}")

    def closeClicked(self):
        sys.exit()