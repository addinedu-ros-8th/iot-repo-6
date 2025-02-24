#ifndef SERVO_PIN
#define SERVO_PIN 6
#endif

#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

bool isRegisteredUID(String receivedUID);

extern MFRC522 rfid; // RFID 객체는 RFID_read.h에서 정의
extern Servo myServo;  // 메인 파일에서 정의됨

byte registeredUID[4] = {0x76, 0x89, 0xCE, 0x01};
bool servoPosition = false;

void rfidTagServoSetup() {
    myServo.attach(SERVO_PIN);
    myServo.write(0);
    Serial.println("RFID Servo Initialized");
}

String rfidTagServoLoop() {
    if (Serial.available() > 0) {
        String receivedUID = Serial.readStringUntil('\n');
        receivedUID.trim();

        if (isRegisteredUID(receivedUID)) {
            myServo.write(servoPosition ? 0 : 90);
            servoPosition = !servoPosition;
            return "{\"rfid_status\":\"Active door\", \"servo_angle\":" + String(myServo.read()) + "}";
        } else {
            return "{\"error\":\"Not registered card\"}";
        }
    }
    return "{}";
}

bool isRegisteredUID(String receivedUID) {
    String registeredUIDStr = "";
    for (byte i = 0; i < 4; i++) {
        registeredUIDStr += String(registeredUID[i], HEX);
    }
    return receivedUID.equalsIgnoreCase(registeredUIDStr);
}
