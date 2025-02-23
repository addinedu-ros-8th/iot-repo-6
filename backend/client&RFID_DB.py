import serial
import time
import mysql.connector

arduino = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# MySQL 연결 설정
# db = mysql.connector.connect(
#     host="localhost",    
#     user="root",         
#     password="password", 
#     database="smart_farm" 
# )

cursor = db.cursor()

time.sleep(2) 

def send_uid_to_arduino(uid):
    arduino.write(uid.encode())  
    print(f"Sent UID to Arduino: {uid}")

def check_rfid_data():
    while True:
        cursor.execute("SELECT uid FROM rental_kit ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()

        if result:
            uid = result[0]  
            print(f"Fetched UID from DB: {uid}")
            send_uid_to_arduino(uid)  
        time.sleep(5)  

while True:
    check_rfid_data()