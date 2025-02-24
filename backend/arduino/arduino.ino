<<<<<<< HEAD
// arduino.ino - 메인 파일
void setup() {
    Serial.begin(115200);
=======
#include "RFID_TAG_servomotor.h"
#include "RFID_tag_read.h"
#include "atmosphere_temp_hum_sensor.h"
#include "light_control_sensor.h"
#include "stepper_motor_with_camera.h"
#include "water_level_senser.h"
#include "water_pump_with_plants_table.h"

void setup() {
    Serial.begin(9600);
>>>>>>> refs/remotes/origin/main
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
<<<<<<< HEAD
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
=======

    delay(30000);
}
>>>>>>> refs/remotes/origin/main
