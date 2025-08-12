#include <WiFi.h>

const char* ssid = "host";
const char* password = "password";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  Serial.println(WiFi.localIP());
}

void loop() {

}