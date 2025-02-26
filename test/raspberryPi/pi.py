import socket
import threading
import serial

# 설정
SERVER_IP = '192.168.0.155'
PORT = 3306
ARDUINO_PORT = '/dev/ttyACM0'  # 아두이노가 연결된 포트
BAUD_RATE = 9600

# 소켓 설정 (PC와의 통신)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print(f"PC server {SERVER_IP}:{PORT} on")

# 시리얼 설정 (아두이노와의 통신)
ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
print("Arduino connected on", ARDUINO_PORT)

# PC에서 수신한 데이터 처리
def receive_data():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"PC로부터 받은 데이터: {data}")
            # PC에서 받은 데이터를 아두이노로 전송
            ser.write(data.encode())
        except Exception as e:
            print(f"Error in receive_data: {e}")
            break

# 아두이노에서 수신한 데이터 처리
def read_arduino():
    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode().strip()
                if data:
                    print(f"Arduino로부터 받은 데이터: {data}")
                    # 아두이노에서 받은 데이터를 PC로 전송
                    client_socket.sendall(data.encode())
        except Exception as e:
            print(f"Error in read_arduino: {e}")
            break

# PC로 데이터 전송
def send_data():
    while True:
        msg = input("PC 메시지 입력 : ")
        client_socket.sendall(msg.encode())

# 스레드 설정
receive_thread = threading.Thread(target=receive_data)
arduino_thread = threading.Thread(target=read_arduino)
send_thread = threading.Thread(target=send_data)

# 스레드 시작
receive_thread.start()
arduino_thread.start()
send_thread.start()

# 스레드 종료 대기
receive_thread.join()
arduino_thread.join()
send_thread.join()

# 연결 종료
client_socket.close()
ser.close()

