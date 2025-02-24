#ifndef ATMOSPHERE_TEMP_HUM_SENSOR_H
#define ATMOSPHERE_TEMP_HUM_SENSOR_H

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

#endif
