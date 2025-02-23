#include <Stepper.h>

const int stepsPerRevolution = 2048;  // 28BYJ-48 기준
Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); // IN1, IN3, IN2, IN4

void setup() {
  myStepper.setSpeed(10); // 속도 설정 (RPM)
  Serial.begin(9600);
}

void loop() {
  Serial.println("시계 방향 회전");
  myStepper.step(stepsPerRevolution);  // 1바퀴 회전
  delay(1000);

  Serial.println("반시계 방향 회전");
  myStepper.step(-stepsPerRevolution); // 반대 방향 1바퀴 회전
  delay(1000);
}
