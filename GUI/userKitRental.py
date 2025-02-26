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
        # 이미 대여된 farm_kit_id 가져오기
        query = "SELECT farm_kit_id FROM rental_kit"
        self.db.cursor.execute(query)
        rented_kits = {row[0] for row in self.db.cursor.fetchall()}  # 집합(set)으로 저장

        labels = [self.num_1, self.num_2, self.num_3, self.num_4]
        checkboxes = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4]

        # 체크박스 상태 업데이트
        for i in range(4):  # 1~4번 farm_kit_id 기준
            farm_kit_id = i + 1  
            if farm_kit_id in rented_kits:
                checkboxes[i].setChecked(True)
                checkboxes[i].setEnabled(False)  # 대여된 키트는 체크 후 비활성화
                labels[i].setText(f"농장 키트 ID: {farm_kit_id} (대여됨)")
            else:
                checkboxes[i].setChecked(False)
                checkboxes[i].setEnabled(True)  # 대여되지 않은 키트는 선택 가능
                labels[i].setText(f"농장 키트 ID: {farm_kit_id} (대여 가능)")

    def save_rental_kit(self):
        """체크된 키트를 rental_kit 테이블에 저장"""
        if not self.dateEdit.date().isValid():
            QMessageBox.warning(self, "경고", "날짜를 선택하세요")
            return

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

        # 키트 대여 처리
        for kit_id in selected_kits:
            self.db.cursor.execute(
                "INSERT INTO rental_kit (user_id, farm_kit_id, rental_kit_status_id, rental_startdate) VALUES (%s, %s, %s, %s)",
                (self.user_num, kit_id, unavailable_status, rent_startdate)
            )
            self.db.commit()

        QMessageBox.information(self, "성공", "대여가 완료되었습니다.")
        self.update_labels()  # UI 업데이트