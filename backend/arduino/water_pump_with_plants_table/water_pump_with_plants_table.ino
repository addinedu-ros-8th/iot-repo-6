#define SOIL_MOISTURE A0  // 토양 습도 센서 핀
#define WATER_PUMP 4      // 펌프 핀

void setup() {
    Serial.begin(9600);
    pinMode(WATER_PUMP, OUTPUT);
    digitalWrite(WATER_PUMP, LOW);  // 펌프 초기 상태 OFF
}

void loop() {
    int soilMoisture = analogRead(SOIL_MOISTURE);  // 토양 습도 값 읽기
    Serial.print("Soil Moisture: ");
    Serial.println(soilMoisture);  // 값 출력

    if (soilMoisture == 0) {
        digitalWrite(WATER_PUMP, HIGH);  // 습도가 0이면 펌프 ON
        Serial.println("WATER_PUMP ON");
    } 
    else if (soilMoisture >= 100) {
        digitalWrite(WATER_PUMP, LOW);  // 습도가 100 이상이면 펌프 OFF
        Serial.println("WATER_PUMP OFF");
    }

    delay(1000);  // 1초마다 측정
}
