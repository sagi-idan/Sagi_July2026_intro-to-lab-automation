

// the setup function runs once when you press reset or power the board
const int ledPin=4;
const int buttonPin=6;
const int interruptPin = 2; // pins 2 or 3 can be used

int lastButtonState =LOW;

void setup() { 
  pinMode(ledPin, OUTPUT);  // initialize led pin as output
  pinMode(buttonPin, INPUT);  //initialize interrupt pin as input
  Serial.begin(9600);

}

// the loop function runs over and over again forever
void loop() {
int currentButtonState = digitalRead(buttonPin);

//for (int i = 0; i< 10000; i++){
//    Serial.println("calculating " +String(i)+ "...");
//}


if (currentButtonState == HIGH) {
  digitalWrite(ledPin, HIGH);
  Serial.println("Pressed");
} 
else {
  digitalWrite(ledPin, LOW);
  Serial.println("Released");


  }

}          

