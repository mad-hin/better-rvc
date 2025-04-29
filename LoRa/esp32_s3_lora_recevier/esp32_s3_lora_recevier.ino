#include <SPI.h>
#include <LoRa.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int SW2 = 12; 
const int SW3 = 13; 

#define ss 5
#define rst 14
#define dio0 2
#define RESET_TIMEOUT_MS 5000  // Reset if no message received for 2 seconds

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

unsigned long lastReceivedTime = 0;

int ch1_rssi = 0;
int ch2_rssi = 0;

void setup() {
  Serial.begin(115200);

  pinMode(SW2, INPUT_PULLUP);
  pinMode(SW3, INPUT_PULLUP);

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
  // Check for incoming messages
  if (LoRa.parsePacket()) {
    Serial.print("Received packet: '");
    while (LoRa.available()) {
      String data = LoRa.readString();
      Serial.print(data);

      // get ch1 and ch2 rssi 
      if (data.startsWith("S") && data.charAt(1) == ('0' + 1)) {
        ch1_rssi = LoRa.packetRssi();
        
      } else if (data.startsWith("S") && data.charAt(1) == ('0' + 2)){
        ch2_rssi = LoRa.packetRssi();

      }
    }
    Serial.print("' (RSSI: ");
    Serial.print(LoRa.packetRssi());
    Serial.println(")");

    Serial.println(String("Ch1 RSSI: ")+ch1_rssi);
    Serial.println(String("Ch2 RSSI: ")+ch2_rssi);

    lastReceivedTime = millis();  // Reset watchdog timer
  }
  
  // TFT display of ch1 and ch2 RSSI value
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("Ch1 RSSI: "+ String(ch1_rssi));
  display.setCursor(0, 12);
  display.println("Ch2 RSSI: "+ String(ch2_rssi));

  // compare ch1 or ch2 is closer
  display.setCursor(0, 24);
  if(ch1_rssi > ch2_rssi){
    // Serial.println("Ch1 closer");
    display.println("Ch1 closer");
  } else{
    // Serial.println("Ch2 closer");
    display.println("Ch2 closer");
  }
  

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
  // For Arduino, use: asm volatile ("jmp 0"); 
}