#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10  
#define RST_PIN 9    

MFRC522 rfid(SS_PIN, RST_PIN); // 한 곳에서만 선언

void rfidTagReadSetup() {
    SPI.begin();
    rfid.PCD_Init();
    Serial.println("RFID Reader Initialized");
}

void rfidTagReadLoop() {
    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
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
    delay(500);
}
