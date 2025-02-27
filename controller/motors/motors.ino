#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <Stepper.h>

// 서보모터: door motor
// 스텝모터: camera motor

#define SS_PIN 10  
#define RST_PIN 9    
#define DOOR_MOTOR_PIN 8  // 서보모터 핀

MFRC522 rfid(SS_PIN, RST_PIN);
Servo doorMotor;

// ✅ camera motor (스텝모터 핀 1~4 설정)
#define STEPS_PER_REV 2048  // 28BYJ-48 기준
#define STEPS_PER_DEGREE (STEPS_PER_REV / 360)  
Stepper cameraMotor(STEPS_PER_REV, 1, 3, 2, 4); // IN1, IN3, IN2, IN4 (핀 1, 2, 3, 4 사용)

bool isDoorOpen = false;  // 문 상태 (false: 닫힘, true: 열림)
unsigned long lastRFIDTime = 0;
const unsigned long rfidCheckInterval = 200;  // RFID 체크 주기 (200ms)

int currentCameraFlag = 1;  
int currentCameraAngle = 0;  

void setup() {
    Serial.begin(9600);  // 시리얼 통신 속도 설정
    SPI.begin();
    rfid.PCD_Init();
    
    doorMotor.attach(DOOR_MOTOR_PIN);
    doorMotor.write(0);  // 기본 위치 0도 (닫힘)

    cameraMotor.setSpeed(15);  // 스텝모터 속도 설정

    Serial.println("✅ Ready for commands.");
}

void loop() {
    unsigned long currentMillis = millis();

    // ✅ Python에서 "OPEN" 신호 수신 시 서보모터 동작
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();  // 개행 문자 제거

        // ✅ door motor (서보모터) 제어
        if (command == "OPEN") {
            toggleDoor();  // 문 상태 변경 함수 호출
        }

        // ✅ camera motor (스텝모터) 제어
        else if (command.startsWith("CAMERA FLAG ")) {
            int flag = command.substring(12).toInt();
            moveCameraMotor(flag);
        }
    }
    
    // ✅ RFID 판독 (200ms마다 실행)
    if (currentMillis - lastRFIDTime >= rfidCheckInterval) {
        lastRFIDTime = currentMillis;
        String uid = rfidTagReadLoop();

        if (uid != "None") {  // UID 감지 시 Python으로 전송 (등록 여부는 Python에서 확인)
            Serial.println("{\"uid\":\"" + uid + "\"}");
        }
    }
}

// ----- door motor (서보모터) 제어 -----
void toggleDoor() {
    if (isDoorOpen) {
        doorMotor.write(0);  
        Serial.println("DOOR CLOSED");
    } else {
        doorMotor.write(90);  
        Serial.println("DOOR OPENED");
    }
    isDoorOpen = !isDoorOpen;
}

// ----- RFID 판독 함수 -----
String rfidTagReadLoop() {
    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
        return "None";
    }

    String uidStr = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        if (rfid.uid.uidByte[i] < 0x10) {
            uidStr += "0";
        }
        uidStr += String(rfid.uid.uidByte[i], HEX);
    }

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();

    return uidStr;
}

// ----- camera motor (스텝모터) 제어 -----
void moveCameraMotor(int flag) {
    if (flag < 1 || flag > 5) {
        Serial.println("⚠️ Invalid flag (1~5 required)");
        return;
    }

    int targetAngle = 0;
    if (flag == 1) targetAngle = 45;
    else if (flag == 2) targetAngle = 135;
    else if (flag == 3) targetAngle = 255;
    else if (flag == 4) targetAngle = 315;
    else targetAngle = 0;

    int angleDifference = targetAngle - currentCameraAngle;

    if (angleDifference > 180) angleDifference -= 360;
    else if (angleDifference < -180) angleDifference += 360;

    int stepsToMove = angleDifference * STEPS_PER_DEGREE;

    Serial.print("Moving camera motor to flag ");
    Serial.println(flag);
    cameraMotor.step(stepsToMove);
    delay(1000);

    currentCameraAngle = targetAngle;
    currentCameraFlag = flag;

    Serial.println("✅ Camera motor move complete");
}