const int ledPin = 4;
const int interruptPin = 2;
#include <MsTimer2.h>


void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT);

  MsTimer2::set(30, TurnOff);

  Serial.begin(9600);

  attachInterrupt(digitalPinToInterrupt(interruptPin), buttonISR, RISING); // attach interrupt to the pin - whaen button pressed run the buttonISR function
}

void loop() {

 for (int i = 0; i < 1000; i++) {
   Serial.println("calculating " + String(i) + "...");
 }

}

void buttonISR() {
  MsTimer2::start();
  digitalWrite(ledPin, HIGH);
  
  //digitalWrite(ledPin, LOW);
  
}

void TurnOff()
{
  digitalWrite(ledPin, LOW);
  MsTimer2::stop();
}
