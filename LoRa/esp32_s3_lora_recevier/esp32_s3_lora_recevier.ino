#include <SPI.h>
#include <LoRa.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int SW2 = 12; 
const int SW3 = 13; 
const int HUMAN_SENSOR = 27; 

#define CONTROLLER_ID 3
int closer_to_channel = 0;
String data = "";

#define ss 5
#define rst 14
#define dio0 2
#define RESET_TIMEOUT_MS 5000  // Reset if no message received for 2 seconds

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

unsigned long lastReceivedTime = 0;

void setup() {
  Serial.begin(115200);

  pinMode(SW2, INPUT_PULLUP);
  pinMode(SW3, INPUT_PULLUP);
  pinMode(HUMAN_SENSOR, INPUT);
  while (!Serial);
  Serial.println("LoRa Receiver with Watchdog");

  LoRa.setPins(ss, rst, dio0);
  
  while (!LoRa.begin(433E6)) {
    Serial.println(".");
    delay(500);
  }
  
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initialized!");
  lastReceivedTime = millis();  // Initialize timer

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
  }
  display.clearDisplay();
  display.setRotation(2);
}

void loop() {

  int HUMAN_SENSOR_state = digitalRead(HUMAN_SENSOR);

  // Check for incoming messages
  if (LoRa.parsePacket()) {
    Serial.print("Received packet: '");
    while (LoRa.available()) {
      data = LoRa.readString();
      Serial.print(data);

      // get ch3 data and check which channel is the controller closer to 
      if (data.startsWith("S") && data.charAt(1) == ('0' + CONTROLLER_ID)) {
        // ch1_rssi = LoRa.packetRssi();
        closer_to_channel = data.charAt(3) - '0';
      }

    }
    Serial.print("' (RSSI: ");
    Serial.print(LoRa.packetRssi());
    Serial.println(")");

    Serial.println(String("Closer to ch")+String(closer_to_channel));

    lastReceivedTime = millis();  // Reset watchdog timer
  }

  display.setCursor(90, 0);
  if (HUMAN_SENSOR_state == LOW){
    Serial.println("light!");
    display.println("light!");
  }
  
  // TFT display of received data and the closer channel 
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println(data + " (RSSI: " + LoRa.packetRssi() + ")");
  display.setCursor(0, 12);
  display.println("Closer to ch"+ String(closer_to_channel));
  

  // Check if timeout has occurred
  if (millis() - lastReceivedTime > RESET_TIMEOUT_MS) {
    Serial.println("No messages for 5s! Resetting...");
    softwareReset();  // Custom function to reset
  }

  display.display();
  delay(10);
  display.clearDisplay();
}

// Software reset function
void softwareReset() {
  Serial.println("Rebooting...");
  delay(50);
  ESP.restart();  // For ESP32/ESP8266
}