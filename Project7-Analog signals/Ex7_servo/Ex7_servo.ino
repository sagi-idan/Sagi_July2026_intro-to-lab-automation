
#include <Servo.h>

const int servoPin = 7;
Servo myServo;

const int rotaryPin = A0;
float voltage;
float DA_scaling=5./1024;



void setup() {
  Serial.begin(9600);

  myServo.attach(servoPin);
 }


void loop() {
  // Read potentiometer: approximately 0-1023
  int rotaryValue = analogRead(rotaryPin);


   // Convert 0-1023 to 0-180 degrees
  int angle = map(rotaryValue, 0, 1023, 0, 167);

  // Move the servo
  myServo.write(angle);

  // Print values
  Serial.print("Rotary: ");
  Serial.print(rotaryValue*DA_scaling);
  Serial.print("  Angle: ");
  Serial.println(angle);


}