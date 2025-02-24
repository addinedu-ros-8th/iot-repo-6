#define RELAY_PIN 6  // 릴레이 모듈 핀

void fanSetup() {
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);
}

String fanLoop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        if (command == "ON") {
            digitalWrite(RELAY_PIN, HIGH);
        } else if (command == "OFF") {
            digitalWrite(RELAY_PIN, LOW);
        } else {
            return "error";
        }
    }
    int state = digitalRead(RELAY_PIN);
    String fanStatus = (state == HIGH) ? "ON" : "OFF";
    return "{\"fan_status\":\"" + fanStatus + "\"}";
}
