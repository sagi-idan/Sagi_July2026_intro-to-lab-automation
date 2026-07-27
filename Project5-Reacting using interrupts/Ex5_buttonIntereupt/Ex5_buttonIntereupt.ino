const int ledPin = 4;
const int interruptPin = 2;

volatile bool buttonPressed = false; // volatile so it will always accessed from memory

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT);

  Serial.begin(9600);

  attachInterrupt(digitalPinToInterrupt(interruptPin), buttonISR, CHANGE); // attach interrupt to the pin - whaen button pressed run the buttonISR function
}

void loop() {

  for (int i = 0; i < 10000; i++) {
    Serial.println("calculating " + String(i) + "...");
  }

  
}

void buttonISR() {
  buttonPressed = digitalRead(interruptPin);
  digitalWrite(ledPin, buttonPressed);
}