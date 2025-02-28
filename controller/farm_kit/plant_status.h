#ifndef PLANT_STATUS_H
#define PLANT_STATUS_H

// ----- 온습도 센서 (DHT) -----
#include <DHT.h>
#define DHTPIN 8
#define DHTTYPE DHT11  
DHT dht(DHTPIN, DHTTYPE);

void atmosphereTempHumSetup() {
  dht.begin();
}

float readTemperature() {
  float temp = dht.readTemperature();
  return isnan(temp) ? 0.0 : temp;
}

float readHumidity() {
  float hum = dht.readHumidity();
  return isnan(hum) ? 0.0 : hum;
}

// ----- 조도 및 LED 제어 -----
#define LDR_PIN A3
#define LED_PIN 7

void lightControlSetup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW); // 기본 상태: OFF
}

void setLight(bool state) {
  digitalWrite(LED_PIN, state ? HIGH : LOW);
}

int readLightValue() {
  int lightValue = analogRead(LDR_PIN);
  if (lightValue <= 250) {
      digitalWrite(LED_PIN, HIGH);
  } else {
      digitalWrite(LED_PIN, LOW);
  }
  return lightValue;
}

// ----- 팬 제어 -----
#define RELAY_PIN 6

void fanSetup() {
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);
}

void setFan(bool state) {
    digitalWrite(RELAY_PIN, state ? HIGH : LOW);
}

// ----- 펌프 및 토양 수분 센서 -----
#define SOIL_MOISTURE A0
#define WATER_PUMP 5
#define MOISTURE_THRESHOLD_LOW 300
#define MOISTURE_THRESHOLD_HIGH 700

void waterPumpSetup() {
    pinMode(WATER_PUMP, OUTPUT);
    digitalWrite(WATER_PUMP, LOW); // 기본 상태: OFF
}

void setPump(bool state) {
    digitalWrite(WATER_PUMP, state ? HIGH : LOW);
}

// ✅ **누락된 `readSoilMoisture()` 함수 추가**
int readSoilMoisture() {
    return analogRead(SOIL_MOISTURE);
}

String getPumpState() {
    int soilMoisture = readSoilMoisture();
    String pump_status;
    if (soilMoisture == 0) {
        pump_status = "error";
    } else if (soilMoisture < MOISTURE_THRESHOLD_LOW) {
        digitalWrite(WATER_PUMP, HIGH);
        pump_status = "ON";
    } else if (soilMoisture > MOISTURE_THRESHOLD_HIGH) {
        digitalWrite(WATER_PUMP, LOW);
        pump_status = "OFF";
    } else {
        pump_status = "NO_CHANGE";
    }
    return pump_status;
}

// ----- 명령어 처리 -----
void handleCommand(String command) {
    command.trim();  // 앞뒤 공백 제거

    if (command == "FAN ON") {
        setFan(true);
        Serial.println("{\"status\":\"FAN ON\"}");
    } else if (command == "FAN OFF") {
        setFan(false);
        Serial.println("{\"status\":\"FAN OFF\"}");
    } else if (command == "LIGHT ON") {
        setLight(true);
        Serial.println("{\"status\":\"LIGHT ON\"}");
    } else if (command == "LIGHT OFF") {
        setLight(false);
        Serial.println("{\"status\":\"LIGHT OFF\"}");
    } else if (command == "PUMP ON") {
        setPump(true);
        Serial.println("{\"status\":\"PUMP ON\"}");
    } else if (command == "PUMP OFF") {
        setPump(false);
        Serial.println("{\"status\":\"PUMP OFF\"}");
    } else {
        Serial.println("{\"error\":\"Unknown command\"}");
    }
}

#endif // PLANT_STATUS_H
