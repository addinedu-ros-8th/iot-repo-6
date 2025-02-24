#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10  
#define RST_PIN 9    
#define SERVO_PIN 6  

extern MFRC522 rfid; // 중복 선언 방지
Servo myServo;

byte registeredUID[4] = {0x76, 0x89, 0xCE, 0x01};  

bool servoPosition = false;

void rfidTagServoSetup() {
    myServo.attach(SERVO_PIN);
    myServo.write(0);
    Serial.println("RFID Servo Initialized");
}

void rfidTagServoLoop() {
    if (Serial.available() > 0) {
        String receivedUID = Serial.readStringUntil('\n');
        receivedUID.trim();  

        if (isRegisteredUID(receivedUID)) {
            Serial.println("Active door");
            myServo.write(servoPosition ? 0 : 90);
            servoPosition = !servoPosition;
        } else {
            Serial.println("Not registered card");
        }
    }
}

bool isRegisteredUID(String receivedUID) {
    String registeredUIDStr = "";
    for (byte i = 0; i < 4; i++) {
        registeredUIDStr += String(registeredUID[i], HEX);
    }
    return receivedUID.equalsIgnoreCase(registeredUIDStr);
}
