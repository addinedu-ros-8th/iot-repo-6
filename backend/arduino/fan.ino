#define RELAY_PIN 7  // 릴레이 모듈을 연결한 핀

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // 초기 상태: 모터 OFF
  Serial.begin(9600);  // 라즈베리파이와 시리얼 통신
}

void loop() {
  if (Serial.available()) {  // 시리얼 데이터가 들어오면
    String command = Serial.readStringUntil('\n');  // 개행 문자('\n')까지 읽기
    command.trim();  // 혹시 있을지 모를 공백 제거

    if (command == "ON") {
      digitalWrite(RELAY_PIN, HIGH);  // 모터 ON
    } 
    else if (command == "OFF") {
      digitalWrite(RELAY_PIN, LOW);  // 모터 OFF
    }
  }
}
