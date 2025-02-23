import socket
import threading

SERVER_IP = '192.168.0.155'
PORT = 3306

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
print(f"pc server{SERVER_IP}:{PORT} on")

def receive_data():
	while True:
		try:
			data = client_socket.recv(1024).decode()
			if not data:
				break
			print(f"pc come data : {data}")
		except:
			print("off")
			break
def send_data():
	while True:
		msg = input("PC message :")
		client_socket.sendall(msg.encode())
		
receive_thread = threading.Thread(target = receive_data)
send_thread = threading.Thread(target=send_data)

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

client_socket.close()
