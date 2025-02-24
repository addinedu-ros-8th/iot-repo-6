#define SOIL_MOISTURE A0  // Soil moisture sensor pin
#define WATER_PUMP 5      // Pump pin

// Soil moisture thresholds for turning the pump on/off
#define MOISTURE_THRESHOLD_LOW 300  // Below this, water the plants
#define MOISTURE_THRESHOLD_HIGH 700 // Above this, stop watering

void waterPumpSetup() {
    pinMode(WATER_PUMP, OUTPUT);
    digitalWrite(WATER_PUMP, LOW);  // Pump is off initially
}

void waterPumpLoop() {
    int soilMoisture = analogRead(SOIL_MOISTURE);  // Read soil moisture
    Serial.print("Soil Moisture: ");
    Serial.println(soilMoisture);  // Output moisture level

    if (soilMoisture < MOISTURE_THRESHOLD_LOW) {
        // If soil moisture is too low, turn on the pump
        digitalWrite(WATER_PUMP, HIGH);
        Serial.println("WATER_PUMP ON");
    } 
    else if (soilMoisture > MOISTURE_THRESHOLD_HIGH) {
        // If soil moisture is sufficiently high, turn off the pump
        digitalWrite(WATER_PUMP, LOW);
        Serial.println("WATER_PUMP OFF");
    }

    delay(1000);  // Wait for 1 second before next reading
}
