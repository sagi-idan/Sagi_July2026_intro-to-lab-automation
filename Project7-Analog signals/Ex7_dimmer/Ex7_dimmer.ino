
#include <MD_PWM.h>

const int rotaryPin=A0;
const int ledPin=4;
float voltage;
float DA_scaling=5./1024;


// Create software PWM output on pin 4
MD_PWM ledPWM(ledPin);

void setup() {
  Serial.begin(9600);

  // Start PWM at 200 Hz
  if (!ledPWM.begin(200)) {
    Serial.println("PWM initialization failed");
 }
}

void loop() {
  // Read potentiometer: approximately 0-1023
  int rotaryValue = analogRead(rotaryPin);

  // Convert ADC range 0-1023 to PWM range 0-255
  uint8_t pwmValue = map(rotaryValue, 0, 1023, 0, 255);

  // Set LED brightness
  ledPWM.write(pwmValue);

  // Print values
  Serial.print("Rotary: ");
  Serial.print(rotaryValue*DA_scaling);

  Serial.print("  PWM: ");
  Serial.println(pwmValue);

}