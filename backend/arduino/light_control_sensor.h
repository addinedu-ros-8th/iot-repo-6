#ifndef LIGHT_CONTROL_SENSOR_H
#define LIGHT_CONTROL_SENSOR_H

#define LDR_PIN A3    // LDR 센서가 연결된 핀
#define LED_PIN 7     // LED 제어 핀

void lightControlSetup() {
    pinMode(LED_PIN, OUTPUT);
}

int readLightValue() {
    int lightValue = analogRead(LDR_PIN);
    
    // 예: 어두운 경우 (250 이하) LED ON, 그 외에는 OFF
    if (lightValue <= 250) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }
    return lightValue;
}

#endif // LIGHT_CONTROL_SENSOR_H
