

// the setup function runs once when you press reset or power the board
int ledPin=4;
int refPin=3;
int delay_t=1;
int usec_delay=1;
int counter=0;

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(ledPin, OUTPUT);
  pinMode(refPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
   PORTD |= (1 << PD4) | (1 << PD3); //dont disturb the other pins

  delay(delay_t);

  // Both pins LOW together
  PORTD &= ~((1 << PD4) | (1 << PD3)); //dont turn off the other pins

  delay(delay_t);
}                     

