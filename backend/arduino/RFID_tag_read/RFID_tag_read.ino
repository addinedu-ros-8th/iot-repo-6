#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10    // RFID 모듈의 SDA(SS) 핀
#define RST_PIN 9    // RFID 모들의 RST 핀

MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
    Serial.begin(9600);         // 시리얼 통신 시작
    SPI.begin();                // SPI 통신 시작
    rfid.PCD_Init();            // RFID 초기화
    Serial.println("✅ RFID 리더 준비 완료!");  // 초기 준비 완료 메시지
}

void loop() {
    // RFID 카드 감지 여부 체크
    if (!rfid.PICC_IsNewCardPresent()) {
        return;  // 새 카드가 없으면 함수 종료
    }

    // 카드 읽기
    if (!rfid.PICC_ReadCardSerial()) {
        return;  // 카드 읽기 실패시 함수 종료
    }

    // 카드 UID 출력
    Serial.print("🎫 UID: ");
    for (byte i = 0; i < rfid.uid.size; i++) {
        Serial.print(rfid.uid.uidByte[i] < 0x10 ? "0" : ""); // 두 자릿수로 출력
        Serial.print(rfid.uid.uidByte[i], HEX);               // 16진수로 출력
        Serial.print(" ");
    }
    Serial.println();

    // 태그를 읽은 후 RFID 세션 종료
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();

    delay(500);  // 0.5초 대기 후 다시 읽기
}
