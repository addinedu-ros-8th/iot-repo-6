import time
import serial
import json
from database.database_manager import DB

# 아두이노 시리얼 포트 설정 (포트 이름은 환경에 맞게 수정)
arduino = serial.Serial('/dev/cu.usbmodem101', 9600, timeout=1)
time.sleep(2)  # 연결 안정화 대기

# DB 연결
db = DB(db_name="iot")
db.connect()
db.set_cursor_buffered_true()

# 데이터 수집 및 저장 루프
try:
    while True:
        print("🔄 데이터 수집 중...")
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()  # 아두이노 데이터 읽기
            print("수신된 라인:", line)  # 디버깅용 출력
            try:
                data = json.loads(line)
                # RFID 이벤트 처리: JSON 객체에 "uid" 키가 있으면 RFID 이벤트로 판단
                if "uid" in data:
                    uid = data["uid"]
                    print(f"RFID 이벤트 감지됨: UID={uid}")
                    # 필요한 경우 RFID 이벤트를 별도 테이블에 저장하거나 추가 처리를 수행
                # 센서 데이터 처리: "temp" 키가 있으면 센서 데이터로 판단
                elif "temp" in data:
                    temp = data.get("temp")
                    hum = data.get("hum")
                    light = data.get("light")
                    soilMoisture = data.get("soilMoisture")
                    
                    print(f"받은 센서 값: temp={temp}, hum={hum}, light={light}, soilMoisture={soilMoisture}")
                    
                    # MySQL에 센서 데이터 저장 (4개 데이터)
                    sql = """
                    INSERT INTO plant_status (temperature, humidity, soil_moisture, light_intensity)
                    VALUES (%s, %s, %s, %s)
                    """
                    db.execute(sql, (temp, hum, soilMoisture, light))
                    db.commit()
                    print("센서 데이터베이스에 저장 완료!")
                    
                    # 테스트 SELECT (개발 단계에서만 사용)
                    db.execute("SELECT * FROM plant_status")
                    result = db.fetchall()
                    for row in result:
                        print(row)
                    print("✅ 센서 데이터 저장 테스트 완료!")
                else:
                    print("알 수 없는 데이터:", data)
            except json.JSONDecodeError:
                print("JSON decode error:", line)
        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    print("\n프로그램 종료")
    arduino.close()
    db.close()
