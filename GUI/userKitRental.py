from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from backend.database.database_manager import DB

form_class = uic.loadUiType("userKitRental.ui")[0]

class kitRentWindow(QMainWindow, form_class):

    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Kit Rental")
        
        self.user_id = user_id

        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()

        self.kitRentButton.clicked.connect(self.save_rental_kit)
        self.okBtn.clicked.connect(self.kitRentShow)

        
        self.update_labels()

    def kitRentShow(self):
        print("Kit rent")
        self.close()
        
        from userRegister import userRegisterWindow 
        self.main_window = userRegisterWindow(self.user_id)
        self.main_window.show()

    def update_labels(self):
        query = """SELECT 
            r.farm_kit_id, 
            f.farm_num, 
            r.user_id, 
            u.user_num, 
            r.plant_id, 
            p.plant_name, 
            r.rental_startdate, 
            r.planting_date, 
            rks.rental_kit_status
            FROM 
                rental_kit r
            JOIN 
                farm_kit f ON r.farm_kit_id = f.farm_kit_id
            JOIN 
                user u ON r.user_id = u.user_id
            JOIN 
                plant p ON r.plant_id = p.plant_id
            JOIN 
                rental_kit_status rks ON r.rental_kit_status_id = rks.rental_kit_status_id
            WHERE 
            r.user_id = %s;  -- user_id에 해당하는 데이터 조회"""
        
        self.db.cursor.execute(query, (self.user_id,))
        results = self.db.cursor.fetchall()

        labels = [self.num_1, self.num_2, self.num_3, self.num_4] 
        checkboxes = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4] 

        rented_kit_ids = [row[1] for row in results]

        for i, row in enumerate(results):
            rental_kit_status_id, farm_kit_id, user_id = row
            labels[i].setText(f"Status ID: {rental_kit_status_id}\nFarm Kit ID: {farm_kit_id}\nUser ID: {user_id}")
            checkboxes[i].setEnabled(False)

        for j in range(len(results), 4):
            labels[j].setText("대여 키트 정보 없음")
            checkboxes[j].setEnabled(True)

        if 1 in rented_kit_ids:
            self.checkBox_1.setEnabled(False)
        if 2 in rented_kit_ids:
            self.checkBox_2.setEnabled(False)
        if 3 in rented_kit_ids:
            self.checkBox_3.setEnabled(False)
        if 4 in rented_kit_ids:
            self.checkBox_4.setEnabled(False)


    def save_rental_kit(self):
        selected_kits = [
            self.checkBox_1.isChecked(),
            self.checkBox_2.isChecked(),
            self.checkBox_3.isChecked(),
            self.checkBox_4.isChecked()
        ]

        # 'available' 및 'unavailable' 상태 가져오기
        query_status = "SELECT rental_kit_status_id FROM rental_kit_status WHERE rental_kit_status = %s"
        self.db.cursor.execute(query_status, ('available',))
        available_status = self.db.cursor.fetchone()[0]

        self.db.cursor.execute(query_status, ('unavailable',))
        unavailable_status = self.db.cursor.fetchone()[0]

        # 중복된 대여를 방지하는 쿼리
        check_query = "SELECT * FROM rental_kit WHERE farm_kit_id = %s AND rental_kit_status_id = %s"
        
        # 대여 키트 상태 저장 쿼리
        query = "INSERT INTO rental_kit (user_id, farm_kit_id, rental_kit_status_id) VALUES (%s, %s, %s)"
        
        kit_count = 4
        for kit_id in range(1, kit_count + 1):
            selected_kit = selected_kits[kit_id - 1]

            if selected_kit:
                # 중복 대여가 있는지 확인
                self.db.cursor.execute(check_query, (kit_id, unavailable_status))
                existing_rental = self.db.cursor.fetchone()

                if existing_rental:
                    # 다른 사용자가 이미 대여한 경우
                    QMessageBox.warning(self, "경고", f"키트 {kit_id}는 이미 다른 사용자가 대여했습니다.")
                    getattr(self, f'checkBox_{kit_id}').setChecked(False)  # 선택 해제
                else:
                    # 해당 키트를 unavailable 상태로 저장
                    self.db.cursor.execute(query, (self.user_id, kit_id, unavailable_status))

        self.db.commit()  # DB에 저장
        print("데이터가 삽입되었습니다.")

        # 삽입 후 레이블 및 체크박스 상태 업데이트
        self.update_labels()
