#include <Servo.h>

Servo motor;  // 서보 모터 객체 생성
const int motorPin = 9;  // 모터 연결 핀

void setup() {
    Serial.begin(9600);  // 시리얼 통신 시작
    motor.attach(motorPin);  // 모터 핀 설정
    motor.write(0);  // 모터 초기 상태 OFF
    Serial.println("✅ 아두이노 준비 완료");
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');  // 라즈베리파이에서 명령 수신
        command.trim();  // 불필요한 공백 제거

        if (command == "ON") {
            motor.write(90);  // 모터 ON (각도 90도)
            Serial.println("🚀 모터 ON!");
        }
        else if (command == "OFF") {
            motor.write(0);  // 모터 OFF (각도 0도)
            Serial.println("🛑 모터 OFF!");
        }
    }
}
