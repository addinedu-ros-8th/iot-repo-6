#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11  

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float humi = dht.readHumidity();  
  float temp = dht.readTemperature();

  if (isnan(humi) || isnan(temp)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  Serial.print(analogRead(A0));
  Serial.print(","); 
  Serial.print(humi);
  Serial.print(",");
  Serial.println(temp);

  delay(5000);
}