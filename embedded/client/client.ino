#include <WiFi.h>
#include <WebServer.h>

const char *ssid = "host";
const char *password = "password";

WebServer server(80);

// GPIO pins are not assigned
#define A 0
#define B 0
#define C 0
#define D 0
#define E 0
#define F 0
#define G 0
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

const uint8_t segmentPatterns[13][8] PROGMEM = {
    {0, 0, 0, 0, 0, 0, 1, 1}, // 0
    {1, 0, 0, 1, 1, 1, 1, 1}, // 1
    {0, 0, 1, 0, 0, 1, 0, 1}, // 2
    {0, 0, 0, 0, 1, 1, 0, 1}, // 3
    {1, 0, 0, 1, 1, 0, 0, 1}, // 4
    {0, 1, 0, 0, 1, 0, 0, 1}, // 5
    {0, 1, 0, 0, 0, 0, 0, 1}, // 6
    {0, 0, 0, 1, 1, 1, 1, 1}, // 7
    {0, 0, 0, 0, 0, 0, 0, 1}, // 8
    {0, 0, 0, 0, 1, 0, 0, 1}, // 9
    {0, 0, 0, 1, 0, 0, 1, 1}, // 10 "N"
    {0, 0, 0, 1, 0, 0, 0, 0}, // 11 "R"
    {1, 1, 1, 1, 1, 1, 0, 1}  // 12 "-"
};

const uint8_t segmentPins[8] = {A, B, C, D, E, F, G, DP};

const uint8_t rpmPins[12] = {A0, A1, A2, A3, B0, B1, B2, B3, C0, C1, C2, C3};

uint8_t lastFlag = 0;

struct Packet
{
  int id;
  int gear;
  int flag;
  int rpmValues[12];
  int event;
};

void setNum(uint8_t num)
{
  for (uint8_t i = 0; i < 8; i++)
  {
    digitalWrite(segmentPins[i], HIGH);
  }

  for (uint8_t i = 0; i < 8; i++)
  {
    digitalWrite(segmentPins[i], pgm_read_byte(&segmentPatterns[num][i]));
  }
}

void setColor(uint8_t r, uint8_t g, uint8_t b)
{
  analogWrite(RE, r);
  analogWrite(GR, g);
  analogWrite(BL, b);
}

void setLed(uint8_t values[12])
{
  for (uint8_t i = 0; i < 12; i++)
  {
    analogWrite(rpmPins[i], values[i]);
  }
}

String extractValue(String json, String key)
{
  int startIndex = json.indexOf("\"" + key + "\":") + key.length() + 3;
  if (startIndex == -1)
  {
    return "";
  }
  int endIndex = json.indexOf(",", startIndex);
  if (endIndex == -1)
  {
    endIndex = json.indexOf("}", startIndex);
  }

  String value = json.substring(startIndex, endIndex);
  value.trim();
  return value;
}

void handlePost()
{
  String body = server.arg("plain");
  Packet packet;

  packet.id = extractValue(body, "id").toInt();
  packet.gear = extractValue(body, "gear").toInt();
  packet.flag = extractValue(body, "flag").toInt();

  String rpmValuesString = extractValue(body, "rpm-values");
  int rpmValues[12] = {0};
  int index = 0;
  int startIndex = rpmValuesString.indexOf("[") + 1;
  int endIndex = rpmValuesString.indexOf("]");
  String rpmValuesSubString = rpmValuesString.substring(startIndex, endIndex);
  while (rpmValuesSubString.length() > 0 && index < 12)
  {
    int commaIndex = rpmValuesSubString.indexOf(",");
    if (commaIndex == -1)
    {
      rpmValues[index++] = rpmValuesSubString.toInt();
      break;
    }
    rpmValues[index++] = rpmValuesSubString.substring(0, commaIndex).toInt();
    rpmValuesSubString = rpmValuesSubString.substring(commaIndex + 1);
  }
  memcpy(packet.rpmValues, rpmValues, sizeof(rpmValues));

  packet.event = extractValue(body, "event").toInt();

  Serial.print("Recieved package:");
  Serial.println(packet.id);
}

void handlePacket(Packet packet)
{
  setNum(packet.gear);

  if (packet.event != 1)
  {
    setLed(packet.rpmValues);
  }
  else
  {
    // Rev limiter event
  }

  if (packet.flag != lastFlag)
  {
    lastFlag = packet.flag;

    // Flag event
  }
}

uint8_t limiterBlinkState = 0;
unsigned long limiterPreviousMillis = 0;
const unsigned long limiterInterval = 20;
uint8_t limiterBlinkCount = 0;

void limiter()
{
  unsigned long currentMillis = millis();

  if (currentMillis - limiterPreviousMillis >= limiterInterval) {

  }
}

void setup()
{
  for (uint8_t i = 0; i < 8; i++)
  {
    pinMode(segmentPins[i], OUTPUT);
  }

  for (uint8_t i = 0; i < 12; i++)
  {
    pinMode(rpmPins[i], INPUT);
  }

  pinMode(RE, OUTPUT);
  pinMode(GR, OUTPUT);
  pinMode(BL, OUTPUT);

  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
  }

  Serial.println(WiFi.localIP());

  server.on("/packet", HTTP_POST, handlePost);

  server.begin();
  Serial.println("Server ON");
}

void loop()
{
  server.handleClient();
}