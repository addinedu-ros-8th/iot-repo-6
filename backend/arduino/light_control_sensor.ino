#include <Servo.h>

const int LED_PIN = 7;
const int SERVO_PIN = 6; // Servo 핀을 별도로 설정
Servo myServo;
static int lastAngle = 0;  // 초기값을 0으로 설정

void lightControlSetup() {
  myServo.attach(SERVO_PIN);  // Servo 핀을 별도로 연결
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void moveServo(int targetAngle) {
  if (lastAngle != targetAngle) {
    for (int angle = lastAngle; angle != targetAngle; angle += (targetAngle > lastAngle ? 1 : -1)) {
      myServo.write(angle);
      delay(10);
    }
    lastAngle = targetAngle;  // 각도 업데이트
  }
}

void lightControlLoop() {
  int readValue = analogRead(A1);  // 아날로그 핀에서 값을 읽기
  Serial.println(readValue);

  if (readValue > 700) {
    moveServo(0); 
    digitalWrite(LED_PIN, LOW);  // 밝으면 LED 끄기
  } else if (readValue <= 700 && readValue > 250) {
    moveServo(90);
    digitalWrite(LED_PIN, LOW);  // 중간 밝기일 때 LED 끄기
  } else {
    digitalWrite(LED_PIN, HIGH);  // 어두우면 LED 켜기
  }
}
