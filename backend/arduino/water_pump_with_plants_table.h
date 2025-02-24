#define SOIL_MOISTURE A0  // 토양 수분 센서 핀
#define WATER_PUMP 5      // 펌프 제어 핀

#define MOISTURE_THRESHOLD_LOW 300   // 이 값 미만이면 펌프 ON
#define MOISTURE_THRESHOLD_HIGH 700  // 이 값 초과이면 펌프 OFF

void waterPumpSetup() {
    pinMode(WATER_PUMP, OUTPUT);
    digitalWrite(WATER_PUMP, LOW);  // 초기에는 펌프 OFF
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
