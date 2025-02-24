#include <Stepper.h>

const int stepsPerRevolution = 2048;
const int stepsPerDegree = stepsPerRevolution / 360;

Stepper myStepper(stepsPerRevolution, 1, 2, 3, 4);

int currentFlag = 1;
int currentAngle = 0;

void stepperMotorSetup() {
    myStepper.setSpeed(10);
}

String stepperMotorLoop() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim();
        int flag = input.toInt();

        if (flag < 1 || flag > 4) {
            return "{\"error\":\"Invalid flag\"}";
        }

        int targetAngle = (flag == 1) ? 45 : (flag == 2) ? 135 : (flag == 3) ? 255 : 315;
        int angleDifference = targetAngle - currentAngle;

        if (angleDifference > 180) angleDifference -= 360;
        else if (angleDifference < -180) angleDifference += 360;

        int stepsToMove = angleDifference * stepsPerDegree;
        myStepper.step(stepsToMove);
        delay(1000);

        currentAngle = targetAngle;
        currentFlag = flag;

        return "{\"flag\":" + String(flag) + ",\"angle\":" + String(currentAngle) + "}";
    }
    return "{}";
}
