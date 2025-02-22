#define WATER_LEVEL A0

void setup() {
    Serial.begin(9600);
}

void loop() {
  Serial.print("Water Level: ");
  Serial.println(analogRead(WATER_LEVEL)); 
  delay(1000); 
}