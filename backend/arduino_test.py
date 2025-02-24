import os
import time
import serial
import json
import mysql.connector
from dotenv import load_dotenv

# 아두이노 시리얼 포트 설정 (포트 이름은 환경에 맞게 수정)
arduino = serial.Serial('/dev/cu.usbmodem1101', 9600, timeout=1)
time.sleep(2)  # 연결 안정화 대기

# 환경 변수 로드
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PSWD = os.getenv("DB_PSWD")

# MySQL 연결
db = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PSWD,
    database="iot"
)

if db.is_connected():
    print("✅ 데이터베이스 연결 성공")
else:
    print("❌ 데이터베이스 연결 실패")

cursor = db.cursor()

# 데이터 수집 및 저장 루프
try:
    while True:
        print("🔄 데이터 수집 중...")
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()  # 아두이노 데이터 읽기
            try:
                data = json.loads(line)
                # 각 센서 값 추출 (waterLevel, pumpState는 무시)
                temp = data.get("temp")
                hum = data.get("hum")
                light = data.get("light")
                soilMoisture = data.get("soilMoisture")
                
                print(f"받은 값: temp={temp}, hum={hum}, light={light}, soilMoisture={soilMoisture}")
                
                # MySQL에 데이터 저장 (4개 데이터)
                sql = """
                INSERT INTO plant_status (temperature, humidity, soil_moisture, light_intensity)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (temp, hum, soilMoisture, light))
                db.commit()
                print("데이터베이스에 저장 완료!")
                
                # 테스트 SELECT (개발 단계에서만 사용)
                cursor.execute("SELECT * FROM plant_status")
                result = cursor.fetchall()
                for row in result:
                    print(row)
                print("✅ 데이터베이스에 저장 테스트까지 완료!")
                
            except json.JSONDecodeError:
                print("JSON decode error:", line)
        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    print("\n프로그램 종료")
    arduino.close()
    cursor.close()
    db.close()
