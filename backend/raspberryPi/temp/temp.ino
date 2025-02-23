#include <Stepper.h>

const int stepsPerRevolution = 2048;
Stepper myStepper(stepsPerRevolution,11,9,10,8);

void setup() {
  // put your setup code here, to run once:
  myStepper.setSpeed(17);
}

void loop() {
  // put your main code here, to run repeatedly:
  myStepper.step(stepsPerRevolution);
  delay(200);

  myStepper.step(-stepsPerRevolution);
  delay(200);
}
