import os
import time
import serial
import mysql.connector
from dotenv import load_dotenv

# 🔹 아두이노 시리얼 포트 설정 (리눅스는 '/dev/ttyACM0', 윈도우는 'COMx')
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # 시리얼 연결 안정화 대기

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PSWD = os.getenv("DB_PSWD")

# 🔹 MySQL 데이터베이스 연결
db = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PSWD,
    database="iot"
)

cursor = db.cursor()

# 🔹 데이터 수집 및 저장 루프
try:
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()  # 아두이노 데이터 읽기
            
            soil_moisture_value = int(line.split(",")[0])  # 값 추출
            air_moisture_value = int(line.split(",")[1])
            air_temperature_value = int(line.split(",")[2])

            print(f"받은 값: {soil_moisture_value, air_moisture_value, air_temperature_value}")

            # MySQL에 데이터 저장
            sql = "INSERT INTO soil_test (test_gap) VALUES (%s, %s, %s)"
            cursor.execute(sql, (soil_moisture_value, air_moisture_value, air_temperature_value))
            db.commit()
            print("✅ 데이터베이스에 저장 완료!")

        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    print("\n프로그램 종료")
    arduino.close()
    cursor.close()
    db.close()
