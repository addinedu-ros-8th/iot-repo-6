#include <DHT.h>

#define DHTPIN 8
#define DHTTYPE DHT11  

DHT dht(DHTPIN, DHTTYPE);

void atmosphereTempHumSetup() {
  Serial.begin(9600);
  dht.begin();
}

void atmosphereTempHumLoop() {
  float humi = dht.readHumidity();  
  float temp = dht.readTemperature();

  // 센서 오류 처리
  if (isnan(humi) || isnan(temp)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // 아날로그 값은 제거하고, 온도와 습도만 출력
  Serial.print("Humidity: ");
  Serial.print(humi);
  Serial.print("%, Temperature: ");
  Serial.print(temp);
  Serial.println("°C");

  delay(2000);  // 2초 간격으로 읽기
}
