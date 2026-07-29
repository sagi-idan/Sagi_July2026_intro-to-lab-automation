#include <MsTimer2.h>

// ----------------------
// Pin definitions
// ----------------------
const int LED_PIN = 4;
const int BUTTON_PIN = 2;

// Time (ms) the LED should stay on
volatile unsigned long ledTime = 1000;

// Indicates whether a valid time was received
bool timerConfigured = false;

// ------------------------------------------------
// Setup
// ------------------------------------------------
void setup()
{
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);

  digitalWrite(LED_PIN, LOW);

  Serial.begin(9600);

  // Interrupt on button press
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), buttonISR, RISING);
}


void loop()
{
  // Check if data arrived
  if (Serial.available() > 0)
  {
    // Read until newline
    String input = Serial.readStringUntil('\n');

    input.trim();      // Remove spaces/newlines

    long value = input.toInt();

    // Basic validation
    if (value > 0)
    {
      ledTime = value;

      Serial.print("I received: ");
      Serial.println(ledTime);

      // Configure timer
      // (+1 ms because of the MsTimer2 timing issue)
      MsTimer2::set(ledTime + 1, turn_off);

      timerConfigured = true;
    }
    else
    {
      Serial.println("Invalid input. Enter a positive number.");
    }
  }
}

// ------------------------------------------------
// Interrupt Service Routine
// Runs when the button is pressed
// ------------------------------------------------
void buttonISR()
{
  if (!timerConfigured)
    return;

  digitalWrite(LED_PIN, HIGH);

  // Start countdown
  MsTimer2::start();
}

// ------------------------------------------------
// Timer callback
// Turns LED off when timer expires
// ------------------------------------------------
void turn_off()
{
  digitalWrite(LED_PIN, LOW);

  // Stop timer until next button press
  MsTimer2::stop();
}