#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10  
#define RST_PIN 9    

MFRC522 rfid(SS_PIN, RST_PIN);

void rfidTagReadSetup() {
    SPI.begin();
    rfid.PCD_Init();
    Serial.println("RFID Reader Initialized");
}

String rfidTagReadLoop() {
    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
        return "{}";
    }

    String uidStr = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        if (rfid.uid.uidByte[i] < 0x10) {
            uidStr += "0";
        }
        uidStr += String(rfid.uid.uidByte[i], HEX);
    }
    
    if (uidStr.length() == 0) {
        return "error";
    }
    
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
    delay(500);
    
    return "{\"uid\":\"" + uidStr + "\"}";
}
