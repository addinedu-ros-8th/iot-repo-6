// arduino.ino - 메인 파일
void setup() {
    Serial.begin(115200);
    Serial.println("Smart Farm System Initializing...");

    rfidTagServoSetup();
    atmosphereTempHumSetup();
    lightControlSetup();
    stepperMotorSetup();
    waterLevelSensorSetup();
    waterPumpSetup();
}

void loop() {
    rfidTagServoLoop();
    atmosphereTempHumLoop();
    lightControlLoop();
    stepperMotorLoop();
    waterLevelSensorLoop();
    waterPumpLoop();
}

void rfidTagServoSetup();
void rfidTagServoLoop();
void atmosphereTempHumSetup();
void atmosphereTempHumLoop();
void lightControlSetup();
void lightControlLoop();
void stepperMotorSetup();
void stepperMotorLoop();
void waterLevelSensorSetup();
void waterLevelSensorLoop();
void waterPumpSetup();
void waterPumpLoop();
