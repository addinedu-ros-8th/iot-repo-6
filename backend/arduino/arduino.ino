#include "plant_status.h"  // 센서 및 액추에이터 관련 기능 모두 포함

#ifndef SERVO_PIN
#define SERVO_PIN A2
#endif

#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

Servo myServo;  // 서보 객체

// ----- RFID 관련 코드 (기존 RFID_read.h 내용 통합) -----
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

// ----- 기존 등록 UID 비교 및 서보 관련 함수 -----
byte registeredUID[4] = {0x76, 0x89, 0xCE, 0x01};

bool isRegisteredUID(String receivedUID) {
    String registeredUIDStr = "";
    for (byte i = 0; i < 4; i++) {
        registeredUIDStr += String(registeredUID[i], HEX);
    }
    return receivedUID.equalsIgnoreCase(registeredUIDStr);
}

void rfidTagServoSetup() {
    myServo.attach(SERVO_PIN);
    myServo.write(0);
    Serial.println("RFID Servo Initialized");
}

// ----- setup 및 loop 함수 -----
void setup() {
  Serial.begin(9600);
  
  SPI.begin();
  rfid.PCD_Init();
  Serial.println("Smart Farm System Initializing...");

  // RFID 초기화
  rfidTagServoSetup();
  rfidTagReadSetup();

  // 센서 및 액추에이터 초기화 (plant_status.h에 정의된 함수들)
  atmosphereTempHumSetup();
  lightControlSetup();
  stepperMotorSetup();
  waterLevelSensorSetup();
  waterPumpSetup();
  fanSetup();
}

void loop() {
  // RFID 판독 및 처리
  String rfidData = rfidTagReadLoop();
  if (rfidData != "{}" && rfidData != "error") {
    Serial.println("RFID 데이터 읽음: " + rfidData);
    delay(2000);  // 중복 판독 방지
  }

  // RFID 판독 결과에 따른 서보모터 제어
  rfidData = rfidTagReadLoop();
  if (rfidData != "{}" && rfidData != "error") {
    int uidStart = rfidData.indexOf(":\"") + 2;
    int uidEnd = rfidData.indexOf("\"", uidStart);
    String uid = rfidData.substring(uidStart, uidEnd);
    
    if (isRegisteredUID(uid)) {
      myServo.write(90);  // 등록된 카드이면 90도
      Serial.println("RFID 인식됨: 서보모터 90도");
    } else {
      myServo.write(0);   // 등록되지 않은 카드이면 0도
      Serial.println("등록되지 않은 RFID: 서보모터 0도");
    }
    delay(500);
  } else {
    myServo.write(0);
  }

  // 10초마다 센서 데이터 출력
  static unsigned long lastSensorPrint = 0;
  if (millis() - lastSensorPrint >= 10000) {
    lastSensorPrint = millis();
    
    float temp = readTemperature();
    float hum = readHumidity();
    int lightVal = readLightValue();
    int waterLevel = readWaterLevel();
    int soilMoisture = readSoilMoisture();
    String pumpState = getPumpState();

    String sensorJson = "{";
    sensorJson += "\"temp\":" + String(temp, 2) + ",";
    sensorJson += "\"hum\":" + String(hum, 2) + ",";
    sensorJson += "\"light\":" + String(lightVal) + ",";
    sensorJson += "\"waterLevel\":" + String(waterLevel) + ",";
    sensorJson += "\"soilMoisture\":" + String(soilMoisture) + ",";
    sensorJson += "\"pumpState\":\"" + pumpState + "\"";
    sensorJson += "}";
    
    Serial.println(sensorJson);
  }
}
