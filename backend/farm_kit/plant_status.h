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
// 기존 RELAY_PIN이 SERVO_PIN과 충돌할 수 있으므로 다른 핀으로 재지정 (예: 11)
#define RELAY_PIN 6  

void fanSetup() {
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);
}

String fanLoop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        if (command == "ON") {
            digitalWrite(RELAY_PIN, HIGH);
        } else if (command == "OFF") {
            digitalWrite(RELAY_PIN, LOW);
        } else {
            return "error";
        }
    }
    int state = digitalRead(RELAY_PIN);
    String fanStatus = (state == HIGH) ? "ON" : "OFF";
    return "{\"fan_status\":\"" + fanStatus + "\"}";
}

// ----- 스테퍼 모터 (카메라 관련 제외) -----
#include <Stepper.h>
const int stepsPerRevolution = 2048;
const int stepsPerDegree = stepsPerRevolution / 360;
Stepper myStepper(stepsPerRevolution, 1, 2, 3, 4);
int currentFlag = 1;
int currentAngle = 0;

void stepperMotorSetup() {
    myStepper.setSpeed(10);
}

String stepperMotorLoop() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim();
        int flag = input.toInt();
        if (flag < 1 || flag > 4) {
            return "{\"error\":\"Invalid flag\"}";
        }
        int targetAngle = (flag == 1) ? 45 : (flag == 2) ? 135 : (flag == 3) ? 255 : 315;
        int angleDifference = targetAngle - currentAngle;
        if (angleDifference > 180) angleDifference -= 360;
        else if (angleDifference < -180) angleDifference += 360;
        int stepsToMove = angleDifference * stepsPerDegree;
        myStepper.step(stepsToMove);
        delay(1000);
        currentAngle = targetAngle;
        currentFlag = flag;
        return "{\"flag\":" + String(flag) + ",\"angle\":" + String(currentAngle) + "}";
    }
    return "{}";
}

// ----- 수위 센서 -----
#define WATER_LEVEL A1

void waterLevelSensorSetup() {
  // 별도 초기화 필요 없음
}

int readWaterLevel() {
  int sensorValue = analogRead(WATER_LEVEL);
  int waterLevel = map(sensorValue, 0, 1023, 0, 100);
  return waterLevel;
}

// ----- 펌프 및 토양 수분 센서 -----
#define SOIL_MOISTURE A0
#define WATER_PUMP 5
#define MOISTURE_THRESHOLD_LOW 300
#define MOISTURE_THRESHOLD_HIGH 700

void waterPumpSetup() {
    pinMode(WATER_PUMP, OUTPUT);
    digitalWrite(WATER_PUMP, LOW);
}

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

#endif // PLANT_STATUS_H
