import socket
import threading

# 서버 정보 설정
HOST = '192.168.0.155'  # 모든 네트워크에서 연결 허용
PORT = 3306  # 사용할 포트 번호

# 소켓 생성 및 바인딩
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"📡 서버 시작: {HOST}:{PORT}")

# 클라이언트 연결 대기
client_socket, client_addr = server_socket.accept()
print(f"✅ 클라이언트 연결됨: {client_addr}")

# 데이터 수신 함수
def receive_data():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"📥 라즈베리파이로부터 받은 데이터: {data}")

            # 받은 데이터를 다시 클라이언트로 응답
            response = f"PC에서 받은 메시지: {data}"
            client_socket.sendall(response.encode())
        except:
            print("⚠ 연결 종료")
            break

# 데이터 전송 함수
def send_data():
    while True:
        msg = input("💬 라즈베리파이에 보낼 메시지 입력: ")
        client_socket.sendall(msg.encode())

# 각각의 기능을 별도 스레드에서 실행
receive_thread = threading.Thread(target=receive_data)
send_thread = threading.Thread(target=send_data)

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

client_socket.close()
server_socket.close()
