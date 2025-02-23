#include <Stepper.h>

const int stepsPerRevolution = 2048;  // 28BYJ-48 기준
const int stepsPerDegree = stepsPerRevolution / 360;  // 1도 당 스텝 수

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); // IN1, IN3, IN2, IN4

int flag = 0; // flag 값 초기화

void setup() {
  myStepper.setSpeed(10); // 속도 설정 (RPM)
  Serial.begin(9600); // 시리얼 모니터 시작
  Serial.println("flag 값을 입력하세요 (1~4):");
}

void loop() {
  if (Serial.available() > 0) {
    flag = Serial.parseInt(); // 시리얼 입력받기

    if (flag >= 1 && flag <= 4) {
      int targetAngle = 0;

      // flag 값에 따른 목표 각도 설정
      if (flag == 1) {
        targetAngle = 45;
      } else if (flag == 2) {
        targetAngle = 135;
      } else if (flag == 3) {
        targetAngle = 255;
      } else if (flag == 4) {
        targetAngle = 315;
      }

      // 각도에 해당하는 스텝 수 계산
      int stepsToMove = targetAngle * stepsPerDegree;

      // 설정한 각도만큼 회전
      Serial.print("목표 각도: ");
      Serial.println(targetAngle);
      myStepper.step(stepsToMove);  
      delay(1000);
      Serial.println("다시 flag 값을 입력하세요 (1~4):");
    } else {
      Serial.println("잘못된 flag 값입니다. 1~4 사이의 값을 입력하세요.");
    }
  }
}
