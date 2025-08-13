#include <WiFi.h>
#include <WebServer.h>

const char *ssid = "host";
const char *password = "password";

WebServer server(80);

// GPIO pins are not assigned
#define SA 0
#define SB 0
#define SC 0
#define SD 0
#define SE 0
#define SF 0
#define SG 0
#define DP 0

#define RE 0
#define GR 0
#define BL 0

#define A0 0
#define A1 0
#define A2 0
#define A3 0
#define B0 0
#define B1 0
#define B2 0
#define B3 0
#define C0 0
#define C1 0
#define C2 0
#define C3 0

const uint8_t segmentPatterns[13] PROGMEM = {
  0b00111111,  // 0
  0b00000110,  // 1
  0b01011011,  // 2
  0b01001111,  // 3
  0b01100110,  // 4
  0b01101101,  // 5
  0b01111101,  // 6
  0b00000111,  // 7
  0b01111111,  // 8
  0b01101111,  // 9
  0b00110111,  // 10 "N"
  0b00110000,  // 11 "R"
  0b01000000   // 12 "-"
};

const uint8_t segmentPins[8] = { SA, SB, SC, SD, SE, SF, SG, DP };

const uint8_t rpmPins[12] = { A0, A1, A2, A3, B0, B1, B2, B3, C0, C1, C2, C3 };

uint8_t lastFlag = 0;

struct Packet {
  int id;
  int gear;
  int flag;
  uint8_t rpmValues[12];
  int event;
};

void setNum(uint8_t num) {
  uint8_t pattern = pgm_read_byte(&segmentPatterns[num]);
  for (uint8_t i = 0; i < 8; i++) {
    digitalWrite(segmentPins[i], (pattern >> i) & 0x01);
  }
}

void setColor(uint8_t r, uint8_t g, uint8_t b) {
  analogWrite(RE, r);
  analogWrite(GR, g);
  analogWrite(BL, b);
}

void setLed(uint8_t values[12]) {
  for (uint8_t i = 0; i < 12; i++) {  
    analogWrite(rpmPins[i], values[i]);
  }
}

String extractValue(String json, String key) {
  int startIndex = json.indexOf("\"" + key + "\":") + key.length() + 3;
  int endIndex = json.indexOf(",", startIndex);
  if (endIndex == -1) endIndex = json.indexOf("}", startIndex);
  String value = json.substring(startIndex, endIndex); 
  value.trim();
  return value;
}

void parseRpmValues(String rpmValuesString, int rpmValues[12]) {
  int index = 0;
  rpmValuesString = rpmValuesString.substring(rpmValuesString.indexOf("[") + 1, rpmValuesString.indexOf("]"));
  while (rpmValuesString.length() > 0 && index < 12) {
    int commaIndex = rpmValuesString.indexOf(",");
    rpmValues[index++] = (commaIndex == -1) ? rpmValuesString.toInt() : rpmValuesString.substring(0, commaIndex).toInt();
    rpmValuesString = (commaIndex == -1) ? "" : rpmValuesString.substring(commaIndex + 1);
  }
}

void handlePost() {
  String body = server.arg("plain");
  Packet packet;

  packet.id = extractValue(body, "id").toInt();
  packet.gear = extractValue(body, "gear").toInt();
  packet.flag = extractValue(body, "flag").toInt();

  String rpmValuesString = extractValue(body, "rpm-values");
  int rpmValues[12] = { 0 };
  parseRpmValues(rpmValuesString, rpmValues);
  memcpy(packet.rpmValues, rpmValues, sizeof(rpmValues));

  packet.event = extractValue(body, "event").toInt();

  Serial.print("Received package:");
  Serial.println(packet.id);
}

int limiterBlinkState = 0;
unsigned long limiterPreviousMillis = 0;
const unsigned long limiterInterval = 20;
int limiterBlinkCount = 0;

void limiter() {
  unsigned long currentMillis = millis();

  if (currentMillis - limiterPreviousMillis >= limiterInterval) {
    limiterPreviousMillis = currentMillis;

    uint8_t values[12];

    if (limiterBlinkState == 0) {
      for (uint8_t i = 0; i < 12; i++) {
        values[i] = (i == 0) ? 255 : 0;
      }
      limiterBlinkState = 1;
    } else {
      for (uint8_t i = 0; i < 12; i++) {
        values[i] = 0;
      }
      limiterBlinkState = 0;
      limiterBlinkCount++;
    }

    setLed(values);
  }
}

int flagBlinkState = 0;
unsigned long flagPreviousMillis = 0;
unsigned long flagInterval = 20;
int flagBlinkCount = 0;

void flag(uint8_t r, uint8_t g, uint8_t b) {
  unsigned long currentMillis = millis();
  if (currentMillis - flagPreviousMillis >= flagInterval) {
    flagPreviousMillis = currentMillis;
    setColor(flagBlinkState ? 0 : r, flagBlinkState ? 0 : g, flagBlinkState ? 0 : b);
    flagBlinkState = !flagBlinkState;
    flagBlinkCount++;
  }
}

void handlePacket(Packet packet) {
  setNum(packet.gear);

  if (packet.event == 1) {
    limiterBlinkState = 0;
    limiterPreviousMillis = millis();
    limiterBlinkCount = 0;
    while (limiterBlinkCount < 5) limiter();
  } else {
    setLed(packet.rpmValues);
  }

  if (packet.flag != lastFlag) {
    lastFlag = packet.flag;
    if (packet.flag != 0) {
      flagInterval = (packet.flag == 6) ? 75 : (packet.flag == 7) ? 300 : 150;
      uint8_t r = (packet.flag == 3 || packet.flag == 4 || packet.flag >= 5) ? 255 : 0;
      uint8_t g = (packet.flag == 1 || packet.flag == 3 || packet.flag >= 5) ? 255 : 0;
      uint8_t b = (packet.flag == 2 || packet.flag >= 5) ? 255 : 0;

      flagBlinkState = 0;
      flagPreviousMillis = millis();
      flagBlinkCount = 0;
      while (flagBlinkCount < 3) flag(r, g, b);
    }
  }
}

void setup() {
  for (uint8_t i = 0; i < 8; i++) {
    pinMode(segmentPins[i], OUTPUT);
  }

  for (uint8_t i = 0; i < 12; i++) {
    pinMode(rpmPins[i], OUTPUT);
  }

  pinMode(RE, OUTPUT);
  pinMode(GR, OUTPUT);
  pinMode(BL, OUTPUT);

  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  Serial.println(WiFi.localIP());

  server.on("/packet", HTTP_POST, handlePost);

  server.begin();
  Serial.println("Server ON");
}

void loop() {
  server.handleClient();
}