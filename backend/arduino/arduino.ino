#include "RFID_TAG_servomotor.ino"
#include "RFID_tag_read.ino"
#include "atmosphere_temp_hum_sensor.ino"
#include "light_control_sensor.ino"
#include "stepper_motor_with_camera.ino"
#include "water_level_senser.ino"
#include "water_pump_with_plants_table.ino"

void setup() {
    Serial.begin(9600);
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
