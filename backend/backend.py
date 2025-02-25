import time
import serial
import json
from database.database_manager import DB
from datetime import datetime

# 아두이노 시리얼 포트 설정
kit_arduino = serial.Serial('/dev/cu.usbmodem1401', 115200, timeout=1)
door_arduino = serial.Serial('/dev/cu.usbmodem1301', 9600, timeout=1)
time.sleep(2)  # 연결 안정화 대기

# DB 연결
db = DB(db_name="iot")
db.connect()
db.set_cursor_buffered_true()

# 등록된 RFID UID 목록 가져오기
def get_registered_uids():
    db.execute("SELECT user_card FROM user_card")
    return {row[0] for row in db.fetchall()}

registered_uids = get_registered_uids()

# 데이터 수집 및 저장 루프
try:
    while True:
        print("🔄 데이터 수집 중...")
        
        # 🌱 센서 데이터 수집
        if kit_arduino.in_waiting > 0:
            line = kit_arduino.readline().decode('utf-8', errors="ignore").strip()
            print("[KIT] 수신된 라인:", line)
            try:
                data = json.loads(line)
                if "temp" in data:
                    temp = data.get("temp")
                    hum = data.get("hum")
                    light = data.get("light")
                    soilMoisture = data.get("soilMoisture")
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    print(f"🌡 받은 센서 값: temp={temp}, hum={hum}, light={light}, soilMoisture={soilMoisture}, timestamp={timestamp}")
                    
                    sql = """
                    INSERT INTO plant_status (temperature, humidity, soil_moisture, light_intensity, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    db.execute(sql, (temp, hum, soilMoisture, light, timestamp))
                    db.commit()
                    print("✅ 센서 데이터 저장 완료!")
                else:
                    print("알 수 없는 데이터:", data)
            except json.JSONDecodeError:
                print("JSON decode error:", line)
        
        # 🔑 RFID 데이터 수집 및 서보모터 동작
        if door_arduino.in_waiting > 0:
            line = door_arduino.readline().decode('utf-8').strip()
            print("[DOOR] 수신된 라인:", line)

            try:
                data = json.loads(line)
                uid = data.get("uid")
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if uid:
                    print(f"RFID 이벤트 감지됨: UID={uid}, timestamp={timestamp}")
                    if uid in registered_uids:
                        sql = """
                        INSERT INTO rfid_log (uid, timestamp)
                        VALUES (%s, %s)
                        """
                        db.execute(sql, (uid, timestamp))
                        db.commit()
                        print("✅ RFID 데이터 저장 완료!")

                        # ✅ 등록된 UID일 경우에만 문 열기 명령 전송
                        door_arduino.write(b'OPEN\n')
                    else:
                        print("❌ 미등록 UID - 문 열림 불가")
            except json.JSONDecodeError:
                print("JSON decode error:", line)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("\n프로그램 종료")
    kit_arduino.close()
    door_arduino.close()
    db.close()
