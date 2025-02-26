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
        """렌탈된 키트를 확인하고 체크박스를 조작하는 함수"""
        query = "SELECT farm_kit_id FROM rental_kit"
        self.db.cursor.execute(query)
        rented_kits = {row[0] for row in self.db.cursor.fetchall()}  # 집합(set)으로 저장

        labels = [self.num_1, self.num_2, self.num_3, self.num_4]
        checkboxes = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4]


        for i in range(4): 
            farm_kit_id = i + 1  
            if farm_kit_id in rented_kits:
                checkboxes[i].setChecked(True)
                checkboxes[i].setEnabled(False)
                labels[i].setText(f"농장 키트 ID: {farm_kit_id} (대여됨)")
            else:
                checkboxes[i].setChecked(False)
                checkboxes[i].setEnabled(True)
                labels[i].setText(f"농장 키트 ID: {farm_kit_id} (대여 가능)")
    def save_rental_kit(self):
        """유저가 선택한 키트를 rental_kit 테이블에 저장"""

        if not self.dateEdit.date().isValid():
            QMessageBox.warning(self, "경고", "날짜를 선택하세요")
            return

        rent_startdate = self.dateEdit.date().toString("yyyy-MM-dd")

        checkboxes = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4]
        selected_kits = [i + 1 for i, checkbox in enumerate(checkboxes) if checkbox.isChecked()]

        if not selected_kits:
            QMessageBox.warning(self, "경고", "적어도 하나의 키트를 선택하세요.")
            return

        check_query = "SELECT rental_kit_id, rental_kit_status_id FROM rental_kit WHERE user_id = %s AND farm_kit_id = %s"
        insert_query = """
            INSERT INTO rental_kit (user_id, farm_kit_id, rental_kit_status_id, rental_startdate)
            VALUES (%s, %s, %s, %s)
        """
        update_query = """
            UPDATE rental_kit SET rental_kit_status_id = %s, rental_startdate = %s
            WHERE rental_kit_id = %s AND user_id = %s
        """

        unavailable_status = 2  # 예: 대여 중 상태
        available_status = 1  # 예: 사용 가능 상태

        for kit_id in selected_kits:
            self.db.execute(check_query, (self.user_num, kit_id))
            existing_rentals = self.db.fetchall()  # 여러 개의 키트가 있을 수 있음

            if existing_rentals:
                for rental_kit_id, rental_status in existing_rentals:
                    if rental_status == available_status:
                        self.db.execute(update_query, (unavailable_status, rent_startdate, rental_kit_id, self.user_num))
                        print(f"키트 {kit_id}의 대여 시작 날짜가 수정되었습니다.")
                    else:
                        QMessageBox.warning(self, "경고", f"키트 {kit_id}는 이미 대여된 상태입니다.")
            else:
                self.db.execute(insert_query, (self.user_num, kit_id, unavailable_status, rent_startdate))
                print(f"키트 {kit_id}가 새로 등록되었습니다.")

        self.db.commit()
        QMessageBox.information(self, "성공", "대여가 완료되었습니다.")
        self.update_labels()  # UI 업데이트

    # def save_rental_kit(self):
    #     """체크된 키트를 rental_kit 테이블에 저장"""
    #     if not self.dateEdit.date().isValid():
    #         QMessageBox.warning(self, "경고", "날짜를 선택하세요")
    #         return

    #     rent_startdate = self.dateEdit.date().toString("yyyy-MM-dd")

    #     checkboxes = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4]
        

    #     selected_kits = [i + 1 for i, checkbox in enumerate(checkboxes) if checkbox.isChecked()]

    #     if not selected_kits:
    #         QMessageBox.warning(self, "경고", "적어도 하나의 키트를 선택하세요.")
    #         return

    #     check_query = "SELECT * FROM rental_kit WHERE farm_kit_id = %s"
    #     insert_query = "INSERT INTO rental_kit (user_id, farm_kit_id, rental_kit_status_id, rental_startdate) VALUES (%s, %s, %s, %s)"
    #     update_query = "UPDATE rental_kit SET rental_kit_status_id = %s, rental_startdate = %s WHERE rental_kit_id = %s"

    #     unavailable_status = 2  # 예: 대여 중 상태
    #     available_status = 1  # 예: 사용 가능 상태

    #     for kit_id in selected_kits:
    #         self.db.cursor.execute(check_query, (kit_id,))
    #         existing_rental = self.db.cursor.fetchone()

    #         if existing_rental:
    #             rental_kit_id, _, rental_status, _ = existing_rental
    #             if rental_status == available_status:
    #                 self.db.cursor.execute(update_query, (unavailable_status, rent_startdate, rental_kit_id))
    #                 print(f"키트 {kit_id}의 대여 시작 날짜가 수정되었습니다.")
    #             else:
    #                 QMessageBox.warning(self, "경고", f"키트 {kit_id}는 이미 대여된 상태입니다.")
    #         else:
    #             self.db.cursor.execute(insert_query, (self.user_num, kit_id, unavailable_status, rent_startdate))
    #             print(f"키트 {kit_id}가 새로 등록되었습니다.")

    #         self.db.commit()

    #         QMessageBox.information(self, "성공", "대여가 완료되었습니다.")
    #         self.update_labels()  # UI 업데이트