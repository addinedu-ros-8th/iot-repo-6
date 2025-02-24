import serial
import time
import Adafruit_DHT  # DHT 센서 라이브러리 (설치 필요)

# 아두이노와 연결된 시리얼 포트 (라즈베리파이에 따라 다를 수 있음)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # 시리얼 안정화 대기

# DHT 센서 설정
DHT_SENSOR = Adafruit_DHT.DHT22  # DHT11이면 DHT11로 변경
DHT_PIN = 4  # GPIO 핀 (연결한 핀에 맞게 수정)

THRESHOLD_HUMIDITY = 60  # 이 값보다 높으면 모터 ON

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None:
        print(f"습도: {humidity:.1f}%")
        
        if humidity > THRESHOLD_HUMIDITY:
            arduino.write(b'ON\n')  # 아두이노에 "ON" 전송
            print("모터 ON")
        else:
            arduino.write(b'OFF\n')  # 아두이노에 "OFF" 전송
            print("모터 OFF")
    
    time.sleep(5)  # 5초마다 센서 데이터 확인
