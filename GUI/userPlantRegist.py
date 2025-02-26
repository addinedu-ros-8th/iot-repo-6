import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from userPlantDetail import userPlantDetailWindow
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.database.database_manager import DB

form_class = uic.loadUiType("userPlantRegist.ui")[0]

class userPlantRegistWindow(QMainWindow, form_class):

    def __init__(self,user_num):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Kit Rental Detail")

        self.user_num = user_num

        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()

        self.load_plant_names()

        self.selectButton.clicked.connect(self.kitRentShow)
    
    def kitRentShow(self):
        print("Kit rent detail")
        try:
            selected_plant_nickname = self.textEdit.toPlainText().strip()
            selected_plant_name = self.typeCombo.currentText().strip()
            selected_planting_date = self.dateEdit.date().toString("yyyy-MM-dd")  # 날짜 가져오기

            if not selected_plant_nickname or not selected_plant_name:
                QMessageBox.warning(self, "경고", "식물 별칭과 종류를 입력하세요.")
                return

            print(f"선택된 plant_nickname: {selected_plant_nickname}")  
            print(f"선택된 plant_name: {selected_plant_name}")
            print(f"선택된 planting_date: {selected_planting_date}")


            query = "SELECT plant_id FROM plant WHERE plant_name = %s"
            self.db.execute(query, (selected_plant_name,))
            plant_id_result = self.db.fetchone()

            if not plant_id_result:
                QMessageBox.warning(self, "오류", "선택한 식물이 존재하지 않습니다.")
                return

            plant_id = plant_id_result[0]
            print(f"변환된 plant_id: {plant_id}")
            check_query = "SELECT COUNT(*) FROM rental_kit WHERE user_id = %s"
            self.db.execute(check_query, (self.user_num,))
            user_exists = self.db.fetchone()[0] > 0  # 존재 여부 확인
            if user_exists:
                # 기존 행 업데이트
                update_query = """
                    UPDATE rental_kit
                    SET plant_nickname = %s, plant_id = %s, planting_date = %s
                    WHERE user_id = %s
                """
                self.db.execute(update_query, (selected_plant_nickname, plant_id, selected_planting_date, self.user_num))
                QMessageBox.information(self, "성공", "식물 대여 정보가 업데이트되었습니다.")
            else:
                # 새 행 삽입
                insert_query = """
                    INSERT INTO rental_kit (user_id, plant_nickname, plant_id, planting_date)
                    VALUES (%s, %s, %s, %s)
                """
                self.db.execute(insert_query, (self.user_num, selected_plant_nickname, plant_id, selected_planting_date))
                QMessageBox.information(self, "성공", "식물 대여 정보가 저장되었습니다.")
            self.db.commit()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"식물 선택 실패: {str(e)}")

        self.close()
        self.main_window = userPlantDetailWindow(self.user_num)
        self.main_window.show()

    def load_plant_names(self):
        query = "SELECT plant_name FROM plant;"
        self.db.execute(query)
        result = self.db.fetchall()  
        
        self.typeCombo.clear()
        for row in result:
            self.typeCombo.addItem(row[0])