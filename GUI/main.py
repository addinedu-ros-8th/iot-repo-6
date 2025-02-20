import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from backend.database.database_manager import DB

current_dir = os.path.dirname(os.path.realpath(__file__))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.centralwidget.setStyleSheet("background-color: white;") # 배경색 설정

        logo_image_path = os.path.join(current_dir, "img", "Druid.png")
        pixmap = QPixmap(logo_image_path)

        if pixmap.isNull():
            print("이미지 로드 실패")

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setPixmap(pixmap)

        # 반응형 레이아웃 설정
        layout = QVBoxLayout(self.centralwidget)
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)

        self.centralwidget.setLayout(layout)

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 528, 24))
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
      
    def retranslateUi(self, MainWindow):
          _translate = QCoreApplication.translate
          MainWindow.setWindowTitle(_translate("main", "main"))

if __name__ == "__main__":
    try:
        db = DB()
        db.connect()
    except Exception as e:
        print("Failed to connect to the database")
        print(e)
        sys.exit(1)

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
