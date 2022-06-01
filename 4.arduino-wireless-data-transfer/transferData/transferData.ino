#include <SPI.h>
#include "RF24.h"

RF24 radio(7, 8);
byte address[6] = "1Node";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  radio.begin();
  radio.setPALevel(RF24_PA_LOW);
  radio.openWritingPipe(address);
  radio.startListening();
}

void loop() {
  // using nRF24L01+ for transferring data to another Arduino
  radio.stopListening();
  if(Serial.available()){
      char text = Serial.read();
      radio.write(&text, sizeof(text));
  }
}
