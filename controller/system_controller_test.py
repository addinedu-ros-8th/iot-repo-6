import time
import serial
from database.database_manager import DB

# 아두이노 시리얼 포트 설정
# kit_arduino = serial.Serial('/dev/cu.usbmodem1301', 115200, timeout=1)
# motor_arduino = serial.Serial('/dev/cu.usbmodem1201', 9600, timeout=1)
kit_arduino = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
motor_arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  

# DB 연결
db = DB(db_name="iot")
db.connect()
db.set_cursor_buffered_true()

# 기존 상태 저장용 변수
actuator_states = {}

def get_actuator_status():
    """DB에서 테스트 액추에이터 상태를 가져옴"""
    db.execute("SELECT actuator_name, status FROM test_actuators")
    return {row["actuator_name"]: row["status"] for row in db.fetchall()}

def send_command(device, command):
    """시리얼을 통해 명령어 전송"""
    device.write((command + "\n").encode())
    print(f"📡 Sent: {command}")

try:
    while True:
        # 🔄 DB 상태 주기적으로 확인
        new_states = get_actuator_status()

        for actuator, status in new_states.items():
            if actuator_states.get(actuator) != status:  # 상태 변경 감지
                print(f"🔄 {actuator} 상태 변경 감지: {status}")
                
                if actuator == "WATER_PUMP":
                    send_command(kit_arduino, f"PUMP {status}")
                elif actuator == "RELAY_FAN":
                    send_command(kit_arduino, f"FAN {status}")
                elif actuator == "LED":
                    send_command(kit_arduino, f"LIGHT {status}")
                elif actuator == "DOOR_MOTOR":
                    send_command(motor_arduino, "OPEN" if status == "ON" else "CLOSE")
                elif actuator == "CAMERA_MOTOR":
                    send_command(motor_arduino, f"CAMERA FLAG {status}")  # 카메라 모터 제어
                
                actuator_states[actuator] = status  # 변경된 상태 저장
        
        time.sleep(1) 

except KeyboardInterrupt:
    print("\n테스트 종료")
    kit_arduino.close()
    motor_arduino.close()
    db.close()
