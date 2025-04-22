#include <SPI.h>
#include <LoRa.h>

#define ss 5
#define rst 14
#define dio0 2
#define SENDER_ID 2       // 1 or 2 (lower ID has priority)
#define SEND_AFTER_ID 1
#define TURN_DELAY_MS 500 // Wait after other sender's transmission
#define TIMEOUT_MS 2000   // If no message seen, send anyway
#define JITTER_MS 300     // Max random delay to avoid sync

int counter = 0;
unsigned long lastHeardTime = 0;
bool otherSenderActive = false;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.print("LoRa Sender ");
  Serial.println(SENDER_ID);

  LoRa.setPins(ss, rst, dio0);
  while (!LoRa.begin(433E6)) {
    Serial.println(".");
    delay(500);
  }
  LoRa.setSyncWord(0xF3); // Same for all senders
  Serial.println("LoRa OK!");
}

void loop() {
  // Listen for incoming messages
  receiveMessage();

  // Decide whether to send
  if (shouldSend()) {
    sendMessage();
    lastHeardTime = millis(); // Reset timeout
  }

  // Small delay to prevent CPU overload
  delay(10);
}

// Check if we should send now
bool shouldSend() {
  unsigned long currentTime = millis();
  
  // Case 1: Other sender recently transmitted -> wait our turn
  if (otherSenderActive) {
    if (currentTime - lastHeardTime > TURN_DELAY_MS) {
      otherSenderActive = false;
      return true;
    }
    return false;
  }
  
  // Case 2: Timeout -> send anyway (with random jitter)
  if (currentTime - lastHeardTime > TIMEOUT_MS) {
    delay(random(0, JITTER_MS)); // Small random delay
    return true;
  }
  
  // Case 3: Default -> don't send
  return false;
}

// Send a message
void sendMessage() {
  Serial.print("Sending [");
  Serial.print(counter);
  Serial.println("]");
  
  LoRa.beginPacket();
  LoRa.print("S");
  LoRa.print(SENDER_ID);
  LoRa.print(":");
  LoRa.print(counter);
  LoRa.endPacket();
  
  counter++;
}

// Listen for messages
void receiveMessage() {
  if (LoRa.parsePacket()) {
    String msg = "";
    while (LoRa.available()) {
      msg += (char)LoRa.read();
    }
    
    int rssi = LoRa.packetRssi();
    Serial.print("Heard: ");
    Serial.print(msg);
    Serial.print(" (RSSI: ");
    Serial.print(rssi);
    Serial.println(")");

    // Detect if the other sender transmitted
    if (msg.startsWith("S") && msg.charAt(1) == ('0' + SEND_AFTER_ID)) {
      otherSenderActive = true;
      lastHeardTime = millis();
    }
  }
}