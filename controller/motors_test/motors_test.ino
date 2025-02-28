#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <Stepper.h>

#define SS_PIN 10  
#define RST_PIN 9    
#define DOOR_MOTOR_PIN 8  

#define STEPS_PER_REV 2048  
#define STEPS_PER_DEGREE (STEPS_PER_REV / 360)  
Stepper cameraMotor(STEPS_PER_REV, 1, 3, 2, 4);

MFRC522 rfid(SS_PIN, RST_PIN);
Servo doorMotor;

int currentCameraAngle = 0;

void setup() {
    Serial.begin(9600);
    SPI.begin();
    rfid.PCD_Init();
    
    doorMotor.attach(DOOR_MOTOR_PIN);
    doorMotor.write(0);
    cameraMotor.setSpeed(15);
    
    Serial.println("✅ Motors Test Ready.");
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        
        if (command == "OPEN") {
            doorMotor.write(90);
            Serial.println("{\"status\":\"DOOR OPENED\"}");
        } else if (command == "CLOSE") {
            doorMotor.write(0);
            Serial.println("{\"status\":\"DOOR CLOSED\"}");
        } else if (command.startsWith("CAMERA FLAG ")) {
            int flag = command.substring(12).toInt();
            moveCameraMotor(flag);
        } else {
            Serial.println("{\"error\":\"Unknown command\"}");
        }
    }
}

// ----- camera motor (스텝모터) 제어 -----
void moveCameraMotor(int flag) {
    if (flag < 1 || flag > 5) {
        Serial.println("⚠️ Invalid flag (1~5 required)");
        return;
    }

    int targetAngle = 0;
    if (flag == 1) targetAngle = 45;
    else if (flag == 2) targetAngle = 135;
    else if (flag == 3) targetAngle = 225;  // 기존 255 → 225로 변경 (꼬임 방지)
    else if (flag == 4) targetAngle = 315;
    else targetAngle = 0;

    int angleDifference = targetAngle - currentCameraAngle;

    if (angleDifference > 180) angleDifference -= 360;
    else if (angleDifference < -180) angleDifference += 360;

    int stepsToMove = angleDifference * STEPS_PER_DEGREE;

    Serial.print("Moving camera motor to flag ");
    Serial.println(flag);
    cameraMotor.step(stepsToMove);
    delay(1000);

    currentCameraAngle = targetAngle;
    Serial.println("✅ Camera motor move complete");
}
