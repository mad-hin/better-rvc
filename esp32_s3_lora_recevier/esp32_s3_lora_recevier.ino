#include <SPI.h>
#include <LoRa.h>

#define ss 5
#define rst 14
#define dio0 2
#define RESET_TIMEOUT_MS 5000  // Reset if no message received for 2 seconds

unsigned long lastReceivedTime = 0;

void setup() {
  Serial.begin(115200);
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
}

void loop() {
  // Check for incoming messages
  if (LoRa.parsePacket()) {
    Serial.print("Received packet: '");
    while (LoRa.available()) {
      String data = LoRa.readString();
      Serial.print(data);
    }
    Serial.print("' (RSSI: ");
    Serial.print(LoRa.packetRssi());
    Serial.println(")");
    lastReceivedTime = millis();  // Reset watchdog timer
  }

  // Check if timeout has occurred
  if (millis() - lastReceivedTime > RESET_TIMEOUT_MS) {
    Serial.println("No messages for 2s! Resetting...");
    softwareReset();  // Custom function to reset
  }
}

// Software reset function
void softwareReset() {
  Serial.println("Rebooting...");
  delay(50);
  ESP.restart();  // For ESP32/ESP8266
  // For Arduino, use: asm volatile ("jmp 0"); 
}