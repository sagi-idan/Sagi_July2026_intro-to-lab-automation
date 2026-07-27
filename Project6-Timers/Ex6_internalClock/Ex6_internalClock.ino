const int ledPin = 4;
const int interruptPin = 2;
unsigned long timeCount=0;
unsigned long timeToTurnOff=0;
unsigned long pressTime=0;
int turnOnTime=5000;

volatile bool buttonPressed = false; // volatile so it will always accessed from memory

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(interruptPin, INPUT);

  Serial.begin(9600);

  attachInterrupt(digitalPinToInterrupt(interruptPin), buttonISR, CHANGE); // attach interrupt to the pin - whaen button pressed run the buttonISR function
}

void loop() {

  //for (int i = 0; i < 10000; i++) {
  //  Serial.println("calculating " + String(i) + "...");
  //}
  timeCount=millis();
  Serial.println("time count: "+String(timeCount)+" press time: "+String(pressTime));
  if (timeToTurnOff<timeCount){
    digitalWrite(ledPin, LOW);
  }
}

void buttonISR() {
  //buttonPressed = digitalRead(interruptPin);
  digitalWrite(ledPin, HIGH);
  pressTime=timeCount;
  timeToTurnOff=timeCount+turnOnTime;
  
}