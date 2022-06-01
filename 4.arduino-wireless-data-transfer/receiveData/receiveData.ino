#include <SPI.h>
#include "RF24.h"

// nRF24L01+
RF24 radio(7, 8);
byte address[6] = "1Node";

int redLEDPin = 5;
int greenLEDPin = 2;

// control the fan module L9110
int INA = 9;
int INB = 10;

void setup() {
  // put your setup code here, to run once:
  pinMode(redLEDPin, OUTPUT);
  pinMode(greenLEDPin, OUTPUT);
  pinMode(INA, OUTPUT);
  pinMode(INB, OUTPUT);
  Serial.begin(115200);
  delay(500);
  digitalWrite(redLEDPin, LOW);
  digitalWrite(greenLEDPin, LOW);
  digitalWrite(INB, LOW);
  digitalWrite(INA, HIGH);
  radio.begin();
  radio.setPALevel(RF24_PA_LOW);
  radio.openReadingPipe(1, address);
  radio.startListening();
}

void loop() {
  if(radio.available()){
      char text[32] = "";
      // receive data from other Arduino
      while(radio.available()){
          radio.read(&text, sizeof(text));
      }
      Serial.println(text[0]);
      int earthquake = text[0] - '0';
      // control appliances by "震度"
      if(earthquake >= 4){
        digitalWrite(INA, LOW);
        Serial.println("close the Fan");
      }
      if(earthquake >= 5){
        digitalWrite(redLEDPin, HIGH);
        Serial.println("close Red LED");
      }
      if(earthquake >= 6){
        digitalWrite(greenLEDPin, HIGH);
        Serial.println("close Green LED");
      }
  }
}
