from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from backend.database.database_manager import DB

form_class = uic.loadUiType("userKitRental.ui")[0]

class kitRentWindow(QMainWindow, form_class):

    db = DB(db_name="iot")
    db.connect()
    db.set_cursor_buffered_true()

    def __init__(self, user_id):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Kit Rental")

        self.user_id = user_id

        self.kitRentButton.clicked.connect(self.kitRentShow)
        
        self.update_labels()

    def kitRentShow(self):
        print("Kit rent")
        self.close()
        
        from userRegister import userRegisterWindow 
        self.main_window = userRegisterWindow(self.user_id)
        self.main_window.show()

    def update_labels(self):

        query = """
        SELECT r.rental_kit_status_id, f.farm_kit_id, u.user_id
        FROM rental_kit r
        JOIN farm_kit f ON r.farm_kit_id = f.farm_kit_id
        JOIN user u ON r.user_id = u.user_id
        ORDER BY r.rental_kit_status_id DESC
        LIMIT 4;
        """
        
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchone()

        if result :
            rental_kit_status_id, farm_kit_id, user_id = result

            self.num_1.setText(str(rental_kit_status_id))
            self.num_2.setText(str(farm_kit_id))           
            self.num_3.setText(str(user_id))      
        else :        
            print("데이터 없음")

