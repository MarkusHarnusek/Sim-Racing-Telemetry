#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "host";
const char* password = "password";

WebServer server(80);

void handlePost() {
  String body = server.arg("plain");
  Serial.println(body);
  server.send(200, "text/plain", "Success");
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED) {
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