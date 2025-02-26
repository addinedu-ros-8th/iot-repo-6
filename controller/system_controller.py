import time
import serial
import json
from database.database_manager import DB
from datetime import datetime

# 아두이노 시리얼 포트 설정
kit_arduino = serial.Serial('/dev/cu.usbmodem11201', 115200, timeout=1)
door_arduino = serial.Serial('/dev/cu.usbmodem11301', 9600, timeout=1)
time.sleep(2)  # 연결 안정화 대기

current_kit_num = 1

# DB 연결
db = DB(db_name="iot")
db.connect()
db.set_cursor_buffered_true()

def get_current_plant_info(kit_num):
    """ 현재 farm_kit에 심어진 식물 정보를 가져옴 """
    db.execute("SELECT plant_id FROM rental_kit WHERE farm_kit_id = %s", (kit_num,))
    plant_id_result = db.fetchone()

    if not plant_id_result:
        print(f"⚠️ farm_kit_id={kit_num} 에 해당하는 rental_kit 정보 없음")
        return None

    plant_id = plant_id_result[0]  # plant_id 추출

    # plant 테이블에서 plant_name 및 환경 정보 조회
    db.execute("SELECT * FROM plant WHERE plant_id = %s", (plant_id,))
    plant_data = db.fetchone()

    if not plant_data:
        print(f"⚠️ plant_id={plant_id} 에 해당하는 식물 정보 없음")
        return None

    # 컬럼명 매핑
    keys = ["plant_id", "plant_name", "temperature_min", "temperature_max",
            "humidity_min", "humidity_max", "soil_moisture_min", "soil_moisture_max",
            "light_intensity_min", "light_intensity_max", "growing_date", "harvest_date"]
    
    return dict(zip(keys, plant_data))

# 🌱 현재 farm_kit에 심어진 식물 정보 가져오기 (DB 조회)
plant_env = get_current_plant_info(current_kit_num)

if not plant_env:
    print("⚠️ 현재 설정된 식물이 없습니다. 기본값 유지")
    plant_env = {"plant_name": "DefaultPlant"}  # 기본값 설정

print(f"📌 현재 심어진 식물: {plant_env['plant_name']}")

def set_plant_env(plant_env, temp, hum, light, soil_moisture):
    """ 센서 데이터를 식물 환경 기준과 비교하여 장치를 제어 """
    if not plant_env:
        print("❌ 식물 정보 없음")
        return

    # 온도 제어 (선풍기)
    if temp > plant_env["temperature_max"]:
        kit_arduino.write(b'FAN ON\n')
        print("🌡️ 온도 초과 → 선풍기 ON")
    elif temp < plant_env["temperature_min"]:
        kit_arduino.write(b'FAN OFF\n')
        print("🌡️ 온도 낮음 → 선풍기 OFF")

    # 습도 제어 (가습기) - 아직 미지원
    print(f"💧 습도 값: {hum}")
    
    # 조도 제어 (LED)
    if light > plant_env["light_intensity_max"]:
        kit_arduino.write(b'LIGHT OFF\n')
        print("💡 조도 초과 → 조명 OFF")
    elif light < plant_env["light_intensity_min"]:
        kit_arduino.write(b'LIGHT ON\n')
        print("💡 조도 낮음 → 조명 ON")

    # 토양 수분 제어 (수중 모터)
    if soil_moisture > plant_env["soil_moisture_max"]:
        kit_arduino.write(b'PUMP OFF\n')
        print("💧 토양 수분 초과 → 수중 모터 OFF")
    elif soil_moisture < plant_env["soil_moisture_min"]:
        kit_arduino.write(b'PUMP ON\n')
        print("💧 토양 수분 부족 → 수중 모터 ON")

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
            print(f"[KIT] 수신된 라인: {line}")
            
            try:
                data = json.loads(line)

                # ✅ 명령 상태 응답 처리
                if "status" in data:
                    print(f"✅ 장치 상태 응답: {data['status']}")  # 명령 수행 로그로 변경
                    continue  # 센서 데이터 처리 스킵

                # ✅ 센서 데이터 처리
                if "temp" in data and "hum" in data and "light" in data and "soilMoisture" in data:
                    temp = data["temp"]
                    hum = data["hum"]
                    light = data["light"]
                    soilMoisture = data["soilMoisture"]
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    print(f"🌡 센서 값: temp={temp}, hum={hum}, light={light}, soilMoisture={soilMoisture}")

                    # 환경 기준과 비교하여 장치 제어
                    set_plant_env(plant_env, temp, hum, light, soilMoisture)

                    # ✅ 센서 데이터 저장
                    sql = """
                    UPDATE plant_status
                    SET temperature = %s, humidity = %s, soil_moisture = %s, light_intensity = %s, timestamp = %s
                    WHERE farm_kit_id = %s
                    """
                    db.execute(sql, (temp, hum, soilMoisture, light, timestamp, current_kit_num))
                    db.commit()

                    # ✅ 센서 데이터 로그 저장
                    sql = """
                    INSERT INTO plant_status_log (temperature, humidity, soil_moisture, light_intensity, timestamp, farm_kit_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    db.execute(sql, (temp, hum, soilMoisture, light, timestamp, current_kit_num))
                    db.commit()

                    print("✅ 센서 데이터 저장 완료!")
                else:
                    print("⚠️ 예상되지 않은 데이터 형식:", data)
            except json.JSONDecodeError:
                print("⚠️ JSON decode error:", line)


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
                    sql = """
                    INSERT INTO rfid_log (uid, timestamp)
                    VALUES (%s, %s)
                    """
                    db.execute(sql, (uid, timestamp))
                    db.commit()
                    print("✅ RFID 데이터 저장 완료!")

                    # ✅ 등록된 UID일 경우에만 문 열기 명령 전송
                    if uid in registered_uids:
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
