#ifndef WATER_LEVEL_SENSER_H
#define WATER_LEVEL_SENSER_H

#define WATER_LEVEL A2  // 물 높이 센서 핀 (다른 센서와 충돌 방지)

void waterLevelSensorSetup() {
  // 별도의 초기화가 필요하지 않음.
}

int readWaterLevel() {
  int sensorValue = analogRead(WATER_LEVEL);
  int waterLevel = map(sensorValue, 0, 1023, 0, 100);
  return waterLevel;
}

#endif // WATER_LEVEL_SENSER_H
