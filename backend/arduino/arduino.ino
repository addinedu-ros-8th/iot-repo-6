#include "RFID_control_servomotor.h"
#include "RFID_read.h"
#include "atmosphere_temp_hum_sensor.h"
#include "light_control_sensor.h"
#include "stepper_motor_with_camera.h"
#include "water_level_senser.h"
#include "water_pump_with_plants_table.h"
#include "fan.h"

#include <Servo.h>
Servo myServo;  // extern 선언에 대응하는 정의

void setup() {
  Serial.begin(9600);
  Serial.println("Smart Farm System Initializing...");

  // 각 센서의 setup 함수 호출
  rfidTagServoSetup();
  rfidTagReadSetup();
  atmosphereTempHumSetup();
  lightControlSetup();
  stepperMotorSetup();
  waterLevelSensorSetup();
  waterPumpSetup();
}

void loop() {
  // 각 센서의 데이터를 읽어 변수에 저장하는 함수를 호출
  float temp = readTemperature();
  float hum = readHumidity();
  int lightVal = readLightValue();
  int waterLevel = readWaterLevel();
  int soilMoisture = readSoilMoisture();
  String pumpState = getPumpState();

  // 하나의 JSON 문자열 생성 (모든 데이터를 한 줄의 JSON 객체로 구성)
  String jsonStr = "{";
  jsonStr += "\"temp\":" + String(temp, 2) + ",";
  jsonStr += "\"hum\":" + String(hum, 2) + ",";
  jsonStr += "\"light\":" + String(lightVal) + ",";
  jsonStr += "\"waterLevel\":" + String(waterLevel) + ",";
  jsonStr += "\"soilMoisture\":" + String(soilMoisture) + ",";
  jsonStr += "\"pumpState\":\"" + pumpState + "\"";
  jsonStr += "}";

  Serial.println(jsonStr);

  rfidTagServoLoop();
  rfidTagReadLoop();

  delay(15000);  // 센서 데이터 업데이트 주기 (15초)
}
