#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10  
#define RST_PIN 9    
#define SERVO_PIN 6  

MFRC522 rfid(SS_PIN, RST_PIN);
Servo myServo;


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
  
    if (!rfid.PICC_IsNewCardPresent()) {
        return; 
    }

    if (!rfid.PICC_ReadCardSerial()) {
        return;  
    }


    Serial.print(" UID: ");
    for (byte i = 0; i < rfid.uid.size; i++) {
        Serial.print(rfid.uid.uidByte[i] < 0x10 ? "0" : ""); 
        Serial.print(rfid.uid.uidByte[i], HEX);
        Serial.print(" ");
    }
    Serial.println();


    if (isRegisteredUID()) {
        Serial.println("active door");

        if (servoPosition) {
            myServo.write(0); 
            servoPosition = false;
        } else {
            myServo.write(90); 
            servoPosition = true;
        }
    } else {
        Serial.println("not register card");
    }

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();

    delay(500); 
}

bool isRegisteredUID() {
    for (byte i = 0; i < 4; i++) {
        if (rfid.uid.uidByte[i] != registeredUID[i]) {
            return false;
        }
    }
    return true;
}
