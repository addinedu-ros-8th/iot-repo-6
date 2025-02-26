import sys
import socket
import threading
from PyQt5.QtWidgets import *
from PyQt5 import uic

from_class = uic.loadUiType("project_test.ui")[0]

# 서버 설정
HOST = '192.168.0.155'  # PC의 IP 주소
PORT = 3306

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.button_Clicked)
        
        # 서버 소켓 설정
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()
        print(f"📡 서버 시작: {HOST}:{PORT}, 클라이언트 대기 중...")
        
        # 클라이언트 연결 대기
        self.client_socket, self.client_addr = self.server_socket.accept()
        print(f"✅ 클라이언트 연결됨: {self.client_addr}")

    def button_Clicked(self):
        msg = "ON" if self.pushButton.text() == "Start Motor" else "OFF"
        self.client_socket.sendall(msg.encode())
        self.pushButton.setText("Stop Motor" if msg == "ON" else "Start Motor")
        print(f"🚀 모터 {msg} 신호 전송!")

    def closeEvent(self, event):
        self.client_socket.close()
        self.server_socket.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())