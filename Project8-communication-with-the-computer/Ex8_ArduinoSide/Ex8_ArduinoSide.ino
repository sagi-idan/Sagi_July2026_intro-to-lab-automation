const int ledPin = 4;
const int interruptPin = 2;
int ledTime = 0;

#include <MsTimer2.h>


void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT);
  digitalWrite(ledPin, LOW);


  Serial.begin(9600);

  attachInterrupt(digitalPinToInterrupt(interruptPin), buttonISR, RISING); // attach interrupt to the pin - whaen button pressed run the buttonISR function
}

void loop() {

  if (Serial.available() > 0) {

    // Read a number from the serial port
    String s = Serial.readStringUntil('\n');
    ledTime = s.toInt();

    // Print what was received
    Serial.print("I received: ");
    Serial.println(ledTime);
  }

  MsTimer2::set(ledTime + 1, TurnOff);
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
