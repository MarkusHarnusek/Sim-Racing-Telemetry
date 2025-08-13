#include <WiFi.h>
#include <WebServer.h>

const char *ssid = "host";
const char *password = "password";

WebServer server(80);

struct Packet
{
  int player_car_index;
  int rpm;
  int speed;
  int gear;
  int car_position;
  int pit_limiter;
  bool drs;
  bool drs_allowed;
  int flag;
  int safety_car;
};


void handlePost()
{
  String body = server.arg("plain");              
  Packet packet;
  packet.player_car_index = extractValue(body, "player_car_index").toInt();
  packet.rpm = extractValue(body, "rpm").toInt();
  packet.speed = extractValue(body, "speed").toInt();
  packet.gear = extractValue(body, "gear").toInt();
  packet.car_position = extractValue(body, "car_position").toInt();
  packet.pit_limiter = extractValue(body, "pit-limiter").toInt();
  packet.drs = extractValue(body, "drs") == "true";
  packet.drs_allowed = extractValue(body, "drs_allowed") == "true";
  packet.flag = extractValue(body, "flag").toInt();
  packet.safety_car = extractValue(body, "safety_car").toInt();

  Serial.println("Parsed Packet:");
  Serial.printf("Player Car Index: %d\nRPM: %d\nSpeed: %d\nGear: %d\nCar Position: %d\nPit Limiter: %d\nDRS: %d\nDRS Allowed: %d\nFlag: %d\nSafety Car: %d\n",
                packet.player_car_index, packet.rpm, packet.speed, packet.gear, packet.car_position, packet.pit_limiter, packet.drs, packet.drs_allowed, packet.flag, packet.safety_car);

  server.send(200, "text/plain", "Success");
}

String extractValue(String json, String key) {
  int startIndex = json.indexOf("\"" + key + "\":") + key.length() + 3;
  if (startIndex == -1) return "";
  int endIndex = json.indexOf(",", startIndex);
  if (endIndex == -1) endIndex = json.indexOf("}", startIndex);
  
  // Extract the substring and trim it
  String value = json.substring(startIndex, endIndex);
  value.trim();  // Modify the string in place
  return value;
}

void setup()
{
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
  server.handleClient(); // Handle incoming requests
}