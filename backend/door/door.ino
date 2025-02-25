#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10  
#define RST_PIN 9    
#define SERVO_PIN 8  // 서보모터 핀

MFRC522 rfid(SS_PIN, RST_PIN);
Servo myServo;

bool isDoorOpen = false;  // 문 상태 (false: 닫힘, true: 열림)
unsigned long lastRFIDTime = 0;
const unsigned long rfidCheckInterval = 200;  // RFID 체크 주기 (200ms)

void setup() {
    Serial.begin(9600);  // 시리얼 통신 속도 설정
    SPI.begin();
    rfid.PCD_Init();
    
    myServo.attach(SERVO_PIN);
    myServo.write(0);  // 기본 위치 0도 (닫힘)
}

void loop() {
    unsigned long currentMillis = millis();

    // ✅ Python에서 "OPEN" 신호 수신 시 서보모터 동작
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();  // 개행 문자 제거

        if (command == "OPEN") {
            toggleDoor();  // 문 상태 변경 함수 호출
        }
    }
    
    // ✅ RFID 판독 (200ms마다 실행)
    if (currentMillis - lastRFIDTime >= rfidCheckInterval) {
        lastRFIDTime = currentMillis;
        String uid = rfidTagReadLoop();

        if (uid != "None") {  // UID 감지 시 Python으로 전송 (등록 여부는 Python에서 확인)
            Serial.println("{\"uid\":\"" + uid + "\"}");
        }
    }
}

// ----- 문 상태 변경 함수 -----
void toggleDoor() {
    if (isDoorOpen) {
        myServo.write(0);   // 닫기
        Serial.println("CLOSE");
    } else {
        myServo.write(90);  // 열기
        Serial.println("OPEN");
    }
    isDoorOpen = !isDoorOpen;  // 상태 반전
}

// ----- RFID 데이터 판독 함수 -----
String rfidTagReadLoop() {
    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
        return "None";  // UID가 없으면 "None" 반환
    }

    String uidStr = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        if (rfid.uid.uidByte[i] < 0x10) {
            uidStr += "0";
        }
        uidStr += String(rfid.uid.uidByte[i], HEX);
    }

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();

    return uidStr;
}
