#include <Wire.h>
#include "Adafruit_VL6180X.h"
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define led_SDA_PIN 1 // Change to your desired pin
#define led_SCL_PIN 23 // Change to your desired pin
#define BUZZER_PIN 13
#define PULSE_SENSOR_PIN 6 // Analog pin for pulse rate sensor

#define SERVICE_UUID "0000180d-0000-1000-8000-00805f9b34fb"
#define CHARACTERISTIC_UUID "00002a37-0000-1000-8000-00805f9b34fb"

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
Adafruit_VL6180X vl = Adafruit_VL6180X();
int below60Count = 0;
int repsRemaining = 0;
int setsRemaining = 0;
bool startSensing = false;
int reps, sets, i;
float calo = 0;

BLEServer *pServer;
BLECharacteristic *pCharacteristic;

class MyCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
    std::string value = pCharacteristic->getValue().c_str();
    if (!value.empty()) {
      Serial.println(value.c_str());
      int semicolonIndex = value.find(';');
      if (semicolonIndex != -1) {
        String repsStr = value.substr(0, semicolonIndex).c_str();
        String setsStr = value.substr(semicolonIndex + 1).c_str();
        reps = repsStr.toInt();
        sets = setsStr.toInt();
        Serial.print("Reps: ");
        Serial.println(reps);
        Serial.print("Sets: ");
        Serial.println(sets);
        startSensing = true;
        repsRemaining = reps;
        setsRemaining = sets;
      }
    }
  }
};

// Heart symbol bitmap
static const unsigned char PROGMEM heart[] = {
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000
};

// Fire symbol bitmap
static const unsigned char PROGMEM fire[] = {
  B00011000,
  B00011100,
  B01011010,
  B11011111,
  B11111111,
  B01111110,
  B00111100,
  B00000000
};

void setup() {
  Serial.begin(9600);
  Serial.println("Initializing...");

  Wire.begin(led_SDA_PIN, led_SCL_PIN);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ;
  }

  if (!vl.begin()) {
    Serial.println(F("Failed to find VL6180X sensor"));
    while (1)
      ;
  }
  Serial.println(F("VL6180X sensor found!"));

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(PULSE_SENSOR_PIN, INPUT); // Set pulse sensor pin as input

  BLEDevice::init("FIA");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new BLEServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
      CHARACTERISTIC_UUID, BLECharacteristic::PROPERTY_READ |
                                BLECharacteristic::PROPERTY_WRITE);
  pCharacteristic->addDescriptor(new BLE2902());
  pCharacteristic->setCallbacks(new MyCallbacks());
  pService->start();
  pServer->getAdvertising()->start();
  Serial.println("Bluetooth device active, waiting for connections...");
}

void loop() {
  // Read pulse rate data
  int sensorValue = analogRead(PULSE_SENSOR_PIN);
  int pulseRate = map(sensorValue, 0, 1023, 0, 300);
  pulseRate /= 10;
  if (pulseRate<78)
  {
    pulseRate = 0;
  }
  if (pulseRate > 100) {
        // Stop workout if pulse rate exceeds 100 BPM
        startSensing = false;
        // Beep for 5 seconds
        for (int i = 0; i < 5; i++) {
          digitalWrite(BUZZER_PIN, HIGH);
          delay(500);
          digitalWrite(BUZZER_PIN, LOW);
          delay(500);
        }
  }
  Serial.print("Pulse Rate (BPM): ");
  Serial.println(pulseRate);

  if (startSensing == true) {
    int range = vl.readRange();
    if (range < 80) {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(100);
      digitalWrite(BUZZER_PIN, LOW);
      delay(100);
      if (pulseRate > 100) {
        // Stop workout if pulse rate exceeds 100 BPM
        startSensing = false;
        // Beep for 5 seconds
        for (int i = 0; i < 5; i++) {
          digitalWrite(BUZZER_PIN, HIGH);
          delay(500);
          digitalWrite(BUZZER_PIN, LOW);
          delay(500);
        }
      } else {
        repsRemaining--;
        calo += 0.33;
        if (repsRemaining == 0) {
          digitalWrite(BUZZER_PIN, HIGH);
          delay(1000);
          digitalWrite(BUZZER_PIN, LOW);
          setsRemaining--;
          if (setsRemaining == 0) {
            startSensing = false;
          }
          repsRemaining = reps;
        }

        display.clearDisplay();
        display.setTextSize(2);
        display.setTextColor(SSD1306_WHITE);
        display.setCursor(5, 10);
        display.print("Reps:");
        display.print(repsRemaining);
        
      
        display.display();
      }

    }
    display.clearDisplay();
    display.setTextSize(2);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(5, 10);
    display.print("Reps:");
    display.print(repsRemaining);
    display.setTextSize(1);
    display.setCursor(105, 10);
    display.drawBitmap(105, 20, heart, 8, 8, SSD1306_WHITE); // Draw heart symbol
    display.print(pulseRate);
    display.display();

  }

  if (startSensing == false)
  {
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(3, 10);
    display.print("Calories:");
    display.setTextSize(2);
    display.print(calo);

    display.setTextSize(1);
    display.setCursor(110, 10);
    display.drawBitmap(110, 20, heart, 8, 8, SSD1306_WHITE); // Draw heart symbol
    display.print(pulseRate);
    display.display();
  }

  delay(1000);
}
