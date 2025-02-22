#define PUMP 4 //사용할 펌프의 핀 번호

void setup() {
    Serial.begin(9600);
    pinMode(PUMP, OUTPUT);
    digitalWrite(PUMP, LOW);  // 펌프 끄기
}
void loop() {
   digitalWrite(PUMP, HIGH); //펌프 켜기
  //  digitalWrite(PUMP, LOW); //펌프 끄기
}