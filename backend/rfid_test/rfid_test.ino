#include <SPI.h>
#include <MFRC522.h>
// #include <MFRC522Extended.h>
// #include <deprecated.h>
// #include <require_cpp11.h>

// #define RST_PIN 9
// #define SS_PIN  10

const int RST_PIN = 9;
const int SS_PIN = 10;
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);

  SPI.begin();
  mfrc522.PCD_Init();

  Serial.println("Start!");
}

void loop() {
  String cmd = "";

  while (Serial.available() > 0) {
    cmd = Serial.readStringUntil('\n');  // 줄바꿈 나오기 전까지 문자열 다 읽는거
  }

  if (!mfrc522.PICC_IsNewCardPresent())  // 새 카드 여부 확인
  {
    return;
  }

  if (!mfrc522.PICC_ReadCardSerial())  // 카드 인식했는지 확인
  {
    return;
  }

  if (cmd.length() > 0 && cmd == "write")  // cmd에서 문자열 받은 상태에서, write라고 입력까지 받으면 출력하기
  {
    Serial.print("cmd :");
    Serial.println(cmd);
  } else {
    return;
  }


  const int index = 60;
  MFRC522::StatusCode status;  // 상태 코드


  MFRC522::MIFARE_Key key;  // MIFARE 카드에서 데이터를 읽거나 쓰기 위해 사용하는 암호화 키
  for (int i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }

  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, index, &key, &(mfrc522.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print("Authentication Faild: ");
    Serial.println(mfrc522.GetStatusCodeName(status));

    return;
  }

  char data[16];
  memset(data, 0x00, sizeof(data));

  String name = "milka";
  name.toCharArray(data, name.length() + 1);

  status = mfrc522.MIFARE_Write(index, (byte*)&data, 16);
  if (status != MFRC522::STATUS_OK) {
    Serial.print("Write Failed: ");
    Serial.println(mfrc522.GetStatusCodeName(status));

    return;
  }

  mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
  delay(100);
}