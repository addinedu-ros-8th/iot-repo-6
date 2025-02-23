#include <Servo.h>

const int LED_PIN = 6;
Servo myServo;
static int lastAngle = -1;

void setup() {
  // put your setup code here, to run once:
  myServo.attach(7);
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void moveServo(int targetAngle) {
  if (lastAngle != targetAngle) {
    for (int angle = lastAngle; angle != targetAngle; angle += (targetAngle > lastAngle ? 1 : -1)) {
      myServo.write(angle);
      delay(10);
    }
    lastAngle = targetAngle; // 각도 업데이트
  }
}


void loop() {
  // put your main code here, to run repeatedly:
  int readValue = analogRead(A1);
  Serial.println(readValue);

  if (readValue > 700)
  {
    moveServo(0); 
    digitalWrite(LED_PIN, LOW);
  }
  else if (readValue <= 700 && readValue > 250)
  {
    moveServo(90);
    digitalWrite(LED_PIN, LOW);
  } 
  else
  {
    digitalWrite(LED_PIN, HIGH);
  }
}
