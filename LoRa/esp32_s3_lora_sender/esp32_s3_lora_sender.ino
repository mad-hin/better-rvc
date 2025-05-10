#include <SPI.h>
#include <LoRa.h>
#include <math.h>

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int SW2 = 12; 
const int SW3 = 13; 
const int HUMAN_SENSOR = 27; 

int last_SW2_state = HIGH;
int last_SW3_state = HIGH;

#define ss 5
#define rst 14
#define dio0 2

#define SENDER_ID 1      // 1 or 2 (lower ID has priority)
#define SEND_AFTER_ID 3  // 3 or 1 

#define TURN_DELAY_MS 300 // Wait after other sender's transmission
#define TIMEOUT_MS 1000   // If no message seen, send anyway
#define JITTER_MS 300     // Max random delay to avoid sync

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

int counter = 0;
unsigned long lastHeardTime = 0;
bool otherSenderActive = false;

String msg = "";
double rssi = 0;
double lambda = 3e8/(433e6);
double actual_distance = 0;

void setup() {
  Serial.begin(115200);

  pinMode(SW2, INPUT_PULLUP);
  pinMode(SW3, INPUT_PULLUP);
  // pinMode(HUMAN_SENSOR, INPUT);

  Serial.println("Starting BLE work!");

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

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
  }
  display.clearDisplay();
  display.setRotation(2);
}

void loop() {
  int current_SW2_state = digitalRead(SW2);
  int current_SW3_state = digitalRead(SW3);
  // int HUMAN_SENSOR_state = digitalRead(HUMAN_SENSOR);

  display.setCursor(0, 36);
  if (current_SW2_state == LOW && last_SW2_state == HIGH) {
      Serial.println("Right arrow pressed");
      display.println("SW2 Pressed");
  }

  display.setCursor(0, 48);
  if (current_SW3_state == LOW && last_SW3_state == HIGH){
    Serial.println("Left arraw pressed");
    display.println("SW3 Pressed");
  }

  // display.setCursor(90, 0);
  // if (HUMAN_SENSOR_state == HIGH){
  //   Serial.println("human!");
  //   display.println("human!");
  // }

  // Listen for incoming messages
  receiveMessage();

  // Decide whether to send
  if (shouldSend()) {
    sendMessage();
    lastHeardTime = millis(); // Reset timeout
  }

  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println(String("Sending [") + counter + "]");
  display.setCursor(0, 12);
  display.println(msg + " (RSSI: "+ rssi +")");


  // calculate the distance;
  actual_distance = ((3e8/(433e6))/(4*M_PI))*pow(10,(rssi+12)/(-20));
  // Serial.println(String("distance:") + actual_distance);

  display.setCursor(0, 24);
  display.println("distance: "+ String(actual_distance));
  display.display();



  // Small delay to prevent CPU overload
  last_SW2_state = current_SW2_state;
  last_SW3_state = current_SW3_state;
  delay(10);
  display.clearDisplay();
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
  Serial.println(String("Sending [") + counter + "]");
  
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
    msg = "";
    while (LoRa.available()) {
      msg += (char)LoRa.read();
    }
    
    rssi = LoRa.packetRssi();
    Serial.print("Heard: ");
    Serial.print(msg);
    Serial.print(" (RSSI: ");
    Serial.print(rssi);
    Serial.println(")");

    // display.setTextSize(1);
    // display.setTextColor(WHITE);
    
    // display.display();

    // Detect if the other sender transmitted
    if (msg.startsWith("S") && msg.charAt(1) == ('0' + SEND_AFTER_ID)) {
      otherSenderActive = true;
      lastHeardTime = millis();
    }
  }
}