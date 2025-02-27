#define WATER_PUMP 5
#define RELAY_PIN 6  
#define LED_PIN 7

void setup() {
    Serial.begin(115200);
    Serial.println("🌱 Farm Kit Test Initializing...");
    
    pinMode(WATER_PUMP, OUTPUT);
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);
    
    digitalWrite(WATER_PUMP, LOW);
    digitalWrite(RELAY_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        
        if (command == "PUMP ON") {
            digitalWrite(WATER_PUMP, HIGH);
            Serial.println("{\"status\":\"PUMP ON\"}");
        } else if (command == "PUMP OFF") {
            digitalWrite(WATER_PUMP, LOW);
            Serial.println("{\"status\":\"PUMP OFF\"}");
        } else if (command == "FAN ON") {
            digitalWrite(RELAY_PIN, HIGH);
            Serial.println("{\"status\":\"FAN ON\"}");
        } else if (command == "FAN OFF") {
            digitalWrite(RELAY_PIN, LOW);
            Serial.println("{\"status\":\"FAN OFF\"}");
        } else if (command == "LIGHT ON") {
            digitalWrite(LED_PIN, HIGH);
            Serial.println("{\"status\":\"LIGHT ON\"}");
        } else if (command == "LIGHT OFF") {
            digitalWrite(LED_PIN, LOW);
            Serial.println("{\"status\":\"LIGHT OFF\"}");
        } else {
            Serial.println("{\"error\":\"Unknown command\"}");
        }
    }
}
