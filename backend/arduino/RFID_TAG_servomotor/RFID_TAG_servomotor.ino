#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10  
#define RST_PIN 9    
#define SERVO_PIN 6  

MFRC522 rfid(SS_PIN, RST_PIN);
Servo myServo;

// UID 비교용 등록된 UID
byte registeredUID[4] = {0x76, 0x89, 0xCE, 0x01};  

bool servoPosition = false;  // false = 0°, true = 90°

void setup() {
    Serial.begin(9600);    
    SPI.begin();             
    rfid.PCD_Init();           
    myServo.attach(SERVO_PIN);  
    myServo.write(0);           
    Serial.println("RFID ready to read!");  
}

void loop() {
    if (Serial.available() > 0) {
        String receivedUID = Serial.readStringUntil('\n');
        receivedUID.trim();  
        Serial.print("Received UID from Raspberry Pi: ");
        Serial.println(receivedUID);

        if (isRegisteredUID(receivedUID)) {
            Serial.println("Active door");

            if (servoPosition) {
                myServo.write(0);
                servoPosition = false;
            } else {
                myServo.write(90);
                servoPosition = true;
            }
        } else {
            Serial.println("Not registered card");
        }
    }

    if (!rfid.PICC_IsNewCardPresent()) {
        return; 
    }

    if (!rfid.PICC_ReadCardSerial()) {
        return;  
    }

    Serial.print("UID: ");
    for (byte i = 0; i < rfid.uid.size; i++) {
        Serial.print(rfid.uid.uidByte[i] < 0x10 ? "0" : ""); 
        Serial.print(rfid.uid.uidByte[i], HEX);
        Serial.print(" ");
    }
    Serial.println();
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
}

bool isRegisteredUID(String receivedUID) {
    String registeredUIDStr = "";
    for (byte i = 0; i < 4; i++) {
        registeredUIDStr += String(registeredUID[i], HEX); 
    }

    return receivedUID.equalsIgnoreCase(registeredUIDStr); 
}