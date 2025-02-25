from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from backend.database.database_manager import DB

form_class = uic.loadUiType("userKitRental.ui")[0]

class kitRentWindow(QMainWindow, form_class):

    def __init__(self, user_num):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Kit Rental")
        
        self.user_num = user_num

        self.db = DB(db_name="iot")
        self.db.connect()
        self.db.set_cursor_buffered_true()


        self.kitRentButton.clicked.connect(self.save_rental_kit)
        self.okBtn.clicked.connect(self.kitRentShow)
        self.okBtn.clicked.connect(self.update_labels) 

        self.checkBox_1.stateChanged.connect(self.checkBoxStateChanged)
        self.checkBox_2.stateChanged.connect(self.checkBoxStateChanged)
        self.checkBox_3.stateChanged.connect(self.checkBoxStateChanged)
        self.checkBox_4.stateChanged.connect(self.checkBoxStateChanged)
        
        self.update_labels()

    def kitRentShow(self):
        print("Kit rent")
        self.close()
        
        from userRegister import userRegisterWindow 
        self.main_window = userRegisterWindow(self.user_num)
        self.main_window.show()

    def checkBoxStateChanged(self):
        checkboxes = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4]
        selected_checkbox = self.sender()

        for checkbox in checkboxes:
            if checkbox != selected_checkbox:
                checkbox.setEnabled(False)
            else:
                checkbox.setEnabled(True)

        if not any([checkbox.isChecked() for checkbox in checkboxes]):
            for checkbox in checkboxes:
                checkbox.setEnabled(True)

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
            LEFT JOIN 
                farm_kit f ON r.farm_kit_id = f.farm_kit_id
            LEFT JOIN 
                user u ON r.user_id = u.user_num
            LEFT JOIN 
                plant p ON r.plant_id = p.plant_id
            LEFT JOIN 
                rental_kit_status rks ON r.rental_kit_status_id = rks.rental_kit_status_id;"""
        
        self.db.cursor.execute(query)
        results = self.db.cursor.fetchall()

        labels = [self.num_1, self.num_2, self.num_3, self.num_4] 
        checkboxes = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4] 

        rented_kit_ids = [row[1] for row in results]

        for i, row in enumerate(results):
            (
                farm_kit_id, farm_num, user_id, user_num, plant_id, plant_name, 
                rental_startdate, planting_date, rental_kit_status
            ) = row  

            labels[i].setText(
                f"농장 키트 ID: {farm_kit_id}\n"
                f"농장 번호: {farm_num}\n"
                f"사용자 ID: {user_id}\n"
                f"식물 이름: {plant_name}\n"
                f"대여 시작: {rental_startdate}\n"
                f"식재 날짜: {planting_date}\n"
                f"상태: {rental_kit_status}"
            )
            checkboxes[i].setEnabled(False)

        for j in range(len(results), 4):
            labels[j].setText("대여 키트 정보 없음")
            checkboxes[j].setEnabled(True)

        print(f"rented_kit_ids: {rented_kit_ids}")

        if 1 in rented_kit_ids:
            self.checkBox_1.setEnabled(False)
        if 2 in rented_kit_ids:
            self.checkBox_2.setEnabled(False)
        if 3 in rented_kit_ids:
            self.checkBox_3.setEnabled(False)
        if 4 in rented_kit_ids:
            self.checkBox_4.setEnabled(False)



    def save_rental_kit(self):

        if not self.dateEdit.date().isValid():
            QMessageBox.warning(self, "경고", "날짜를 선택하세요")
            return
        
        selected_kits = [
            self.checkBox_1.isChecked(),
            self.checkBox_2.isChecked(),
            self.checkBox_3.isChecked(),
            self.checkBox_4.isChecked()
        ]

        query_status = "SELECT rental_kit_status_id FROM rental_kit_status WHERE rental_kit_status = %s"
        self.db.cursor.execute(query_status, ('available',))
        available_status = self.db.cursor.fetchone()  
        if available_status:
            available_status = available_status[0]  

        self.db.cursor.execute(query_status, ('unavailable',))
        unavailable_status = self.db.cursor.fetchone() 
        if unavailable_status:
            unavailable_status = unavailable_status[0]

        rent_startdate = self.dateEdit.date().toString("yyyy-MM-dd")

        check_query = "SELECT * FROM rental_kit WHERE farm_kit_id = %s AND rental_kit_status_id = %s"
        insert_query = "INSERT INTO rental_kit (user_id, farm_kit_id, rental_kit_status_id, rental_startdate) VALUES (%s, %s, %s, %s)"
        update_query = "UPDATE rental_kit SET rental_kit_status_id = %s, rental_startdate = %s WHERE rental_kit_id = %s"
        
        kit_count = 4
        for kit_id in range(1, kit_count + 1):
            if selected_kits[kit_id - 1]:
                self.db.cursor.execute(check_query, (self.user_num, kit_id))
                existing_rental = self.db.cursor.fetchone()

                if existing_rental:
                    rental_kit_id, _, rental_status, _ = existing_rental
                    if rental_status == available_status:
                        self.db.cursor.execute(update_query, (rent_startdate, self.user_num, kit_id))
                        self.db.commit()
                        print(f"키트 {kit_id}의 대여 시작 날짜가 수정되었습니다.")
                    else:
                        QMessageBox.warning(self, "경고", f"키트 {kit_id}는 이미 대여된 상태입니다.")
                else: 
                    self.db.cursor.execute(insert_query, (self.user_num, kit_id, unavailable_status, rent_startdate))
                    self.db.commit()
                    print(f"키트 {kit_id}가 새로 등록되었습니다.")

        print("데이터가 삽입되었습니다.")