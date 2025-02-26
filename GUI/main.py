import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from signIn import SignInWindow

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))     # 현재 스크립트의 부모 디렉터리를 sys.path에 추가
from controller.database.database_manager import DB

current_dir = os.path.dirname(os.path.realpath(__file__))   # 현재 파일이 위치한 디렉터리의 절대 경로
from_class = uic.loadUiType(f"{current_dir}/main.ui")[0]    

class Ui_MainWindow(QMainWindow, from_class): 
    def setupUi(self, MainWindow):  
        super().setupUi(MainWindow)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("main", "main"))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setAutoFillBackground(True)

        palette = MainWindow.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        MainWindow.setPalette(palette)

        MainWindow.setMouseTracking(True) 
        self.MainWindow = MainWindow

        logo_image_path = os.path.join(current_dir, "img", "Druid.png")
        pixmap = QPixmap(logo_image_path)

        if pixmap.isNull():
            print("이미지 로드 실패")

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setPixmap(pixmap)

        layout = QVBoxLayout(self.centralwidget)  # 중앙 정렬을 위한 QVBoxLayout 사용
        layout.addWidget(self.label)
        layout.setAlignment(self.label, Qt.AlignCenter)
        self.centralwidget.setLayout(layout)

        # 메뉴바와 상태바 생성 및 스타일 설정
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.setStyleSheet("""
        background-color: white;
        border-radius: 10px;

        QMenuBar { background-color: white; border: none; }
        QStatusBar { background-color: white; border: none; }
        """)

    def show_signin_window(self):
        self.signin_window = SignInWindow()
        self.signin_window.show()
        self.MainWindow.close() 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self) 

    def mousePressEvent(self, event):  # 클릭 시 show_signin_window 호출
        if event.button() == Qt.LeftButton:
            self.ui.show_signin_window()  

if __name__ == "__main__":
    try:
        db = DB()
        db.connect()
    except Exception as e:
        print("Failed to connect to the database")
        print(e)
        sys.exit(1)

    app = QApplication(sys.argv)
    MainWindow = MainWindow() 
    MainWindow.show()  
    sys.exit(app.exec_())
