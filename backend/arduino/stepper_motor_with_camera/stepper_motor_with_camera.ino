#include <Stepper.h>

const int stepsPerRevolution = 2048;  // 28BYJ-48 기준
const int stepsPerDegree = stepsPerRevolution / 360;  // 1도 당 스텝 수

Stepper myStepper(stepsPerRevolution, 8, 10, 9, 11); // IN1, IN3, IN2, IN4

int currentFlag = 1; // 현재 flag 값 (1~4)
int currentAngle = 0; // 현재 각도 (0~360)

void setup() {
  myStepper.setSpeed(10); // 속도 설정 (RPM)
  Serial.begin(9600); // 시리얼 모니터 시작
  Serial.println("flag 값을 입력하세요 (1~4):");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Enter를 기준으로 입력 받기
    int flag = input.toInt();  // 입력 값을 숫자로 변환

    if (flag >= 1 && flag <= 4) {
      int targetAngle = 0;

      // 목표 각도 설정 (flag에 따른 각도)
      if (flag == 1) {
        targetAngle = 45;
      } else if (flag == 2) {
        targetAngle = 135;
      } else if (flag == 3) {
        targetAngle = 255;
      } else if (flag == 4) {
        targetAngle = 315;
      }

      // 현재 각도와 목표 각도의 차이를 계산하여 회전 각도 결정
      int angleDifference = targetAngle - currentAngle;

      // 회전 각도를 -180 ~ +180으로 보정 (줄이 꼬이지 않도록)
      if (angleDifference > 180) {
        angleDifference -= 360;
      } else if (angleDifference < -180) {
        angleDifference += 360;
      }

      // 각도 차이에 해당하는 스텝 수 계산
      int stepsToMove = angleDifference * stepsPerDegree;

      // 설정한 각도만큼 회전
      Serial.print("목표 각도: ");
      Serial.println(targetAngle);
      myStepper.step(stepsToMove);
      delay(1000);

      // 현재 위치 업데이트
      currentAngle = targetAngle;

      // flag 값을 업데이트
      currentFlag = flag;

      Serial.println("다시 flag 값을 입력하세요 (1~4):");
    } else {
      Serial.println("잘못된 flag 값입니다. 1~4 사이의 값을 입력하세요.");
    }
  }
}
