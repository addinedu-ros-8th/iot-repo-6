#define WATER_LEVEL A1

void waterLevelSensorSetup() {
    Serial.begin(9600);
}

void waterLevelSensorLoop() {
  int sensorValue = analogRead(WATER_LEVEL);
  float waterLevel = map(sensorValue, 0, 1023, 0, 100);  // Mapping the sensor value to 0-100% range

  // Print water level as a percentage
  Serial.print("Water Level: ");
  Serial.print(waterLevel);
  Serial.println("%");

  // Example threshold for low water level warning
  if (waterLevel < 20) {
    Serial.println("Warning: Low Water Level!");
  }

  delay(1000);  // Delay before reading the sensor again
}
