from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import datetime
from PyQt5 import uic
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.database.database_manager import DB
# from userKitRentalDetail import userRegisterWindow

form_class = uic.loadUiType("userPlantDetail.ui")[0]

class plantInfoWindow(QMainWindow, form_class):
    def __init__(self,user_num):
        super().__init__()
        self.setupUi(self)

        self.user_num = user_num

        self.get_farm_num()
        self.get_plant_name()
        self.get_planting_days()
        self.update_air_temperature()
        


        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()

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
                 from rental_kit"""
        self.db.cursor.execute(sql, (self.user_num,))
        plant_nickname = self.db.cursor.fetchone()
        self.label2.setText(f"식물 닉네임: {plant_nickname[0]}")

    def get_planting_days(self):
        sql = """SELECT r.planting_date
                 FROM rental_kit r
                 WHERE r.user_id = %s"""
        
        self.db.cursor.execute(sql, (self.user_num,))
        planting_date = self.db.cursor.fetchone()
        planting_date = datetime.strptime(planting_date[0], '%Y-%m-%d')
        current_date = datetime.now()
        days_since_planting = (current_date - planting_date).days
        self.label8.setText(f"--{days_since_planting}일째!")

    def update_air_temperature(self):
        query = """SELECT ki.air_temperature
                FROM rental_kit rk
                JOIN kit_info ki ON rk.rental_kit_id = ki.rental_kit_id
                WHERE rk.rental_kit_id = %s"""
        
        self.db.cursor.execute(query, (self.user_num,))
        air_temperature = self.db.cursor.fetchone()

        self.label3.setText(f"공기 온도: {air_temperature[0]}°C")


    def closeClicked(self):
        sys.exit()