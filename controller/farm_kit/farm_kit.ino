#include "plant_status.h"  // 센서 및 액추에이터 관련 기능 포함

void setup() {
    Serial.begin(115200);  // 시리얼 통신 속도 설정
    Serial.println("🌱 Farm Kit Initializing...");

    // 센서 및 액추에이터 초기화
    atmosphereTempHumSetup();
    lightControlSetup();
    waterPumpSetup();
    fanSetup();
}

unsigned long previousSensorTime = 0;
const unsigned long sensorInterval = 10000;  // 센서 데이터 출력 간격 10초

void loop() {
    unsigned long currentMillis = millis();

    // 센서 데이터 출력 (10초마다)
    if (currentMillis - previousSensorTime >= sensorInterval) {
        previousSensorTime = currentMillis;

        float temp = readTemperature();
        float hum = readHumidity();
        int lightVal = readLightValue();
        int soilMoisture = readSoilMoisture();

        String sensorJson = "{";
        sensorJson += "\"temp\":" + String(temp, 2) + ",";
        sensorJson += "\"hum\":" + String(hum, 2) + ",";
        sensorJson += "\"light\":" + String(lightVal) + ",";
        sensorJson += "\"soilMoisture\":" + String(soilMoisture);
        sensorJson += "}";

        Serial.println(sensorJson);
    }

    // 명령어 수신 및 처리
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');  // 명령어 읽기
        handleCommand(command);  // 명령어 처리
    }
}
