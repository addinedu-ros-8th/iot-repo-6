import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))     # 현재 스크립트의 부모 디렉터리를 sys.path에 추가
from controller.database.database_manager import DB

form_class = uic.loadUiType("adminKit.ui")[0]

class adminKitWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("admin Kit")

        self.exitButton.clicked.connect(self.exitShow)
        self.backButton.clicked.connect(self.backShow)

        self.loadData()


    def exitShow(self):
        print("exit show")
        self.close()

    def backShow(self):
        from adminMain import adminMainWindow  
        self.close()
        self.main_window = adminMainWindow()
        self.main_window.show()

    def loadData(self):
        try:
            db = DB(db_name="iot")
            db.connect()
            db.set_cursor_buffered_true()
            
            query = """
                SELECT 
                    rk.rental_kit_id,
                    rks.rental_kit_status,  -- rental_kit_status 테이블의 상태값
                    fk.farm_num,            -- farm_kit 테이블에서 farm_num 사용
                    u.name AS user_name,    -- user 테이블에서 'name' 컬럼 사용
                    p.plant_name,           -- plant 테이블에서 plant_name 사용
                    rk.rental_startdate,
                    rk.planting_date,
                    ps.temperature,         -- plant_status에서 온도 정보
                    ps.humidity,            -- plant_status에서 습도 정보
                    ps.soil_moisture,       -- plant_status에서 토양 수분
                    ps.light_intensity      -- plant_status에서 빛 강도
                FROM rental_kit rk
                LEFT JOIN rental_kit_status rks ON rk.rental_kit_status_id = rks.rental_kit_status_id
                LEFT JOIN farm_kit fk ON rk.farm_kit_id = fk.farm_kit_id
                LEFT JOIN user u ON rk.user_id = u.user_num  -- user 테이블의 user_num과 연결
                LEFT JOIN plant p ON rk.plant_id = p.plant_id
                LEFT JOIN plant_status ps ON rk.plant_status_id = ps.plant_status_id;
            """
            
            db.execute(query)
            data = db.fetchall()
            # uc.user_card,           -- user_card 테이블에서 user_card 값
#                 LEFT JOIN user_card uc ON rk.user_id = uc.user_card_id
            # 컬럼 이름 설정
            column_names = [
                "Rental Kit ID", "Rental Kit Status", "Farm Kit", "User Name", 
                "Plant", "Rental Start Date", "Planting Date", "Plant Status"
            ]

            # 테이블 위젯 설정
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(column_names))
            self.tableWidget.setHorizontalHeaderLabels(column_names)

            # 데이터 삽입
            for row_idx, row_data in enumerate(data):
                for col_idx, col_value in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_value)))

            db.close()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 불러오기 실패: {str(e)}")
