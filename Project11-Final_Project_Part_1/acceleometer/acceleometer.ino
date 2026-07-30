	
#include "Arduino_SensorKit.h"
 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial);
  
  Accelerometer.begin();

  Oled.begin();
  Oled.setFlipMode(true); // Sets the rotation of the screen
}
 
void loop() {
  // put your main code here, to run repeatedly:
  // 3 axis
  Serial.print("x:"); 
  Serial.print(Accelerometer.readX());  // Read the X Value 
  Serial.print("  ");
  Serial.print("y:"); 
  Serial.print(Accelerometer.readY());  // Read the Y Value       
  Serial.print("  ");
  Serial.print("z:"); 
  Serial.println(Accelerometer.readZ());// Read the Z Value

  	
  int random_value = analogRead(A0);   //read value from A0
 
  Oled.setFont(u8x8_font_chroma48medium8_r); 
  Oled.setCursor(0, 33);    // Set the Coordinates 
  Oled.print("Analog Value:");   
  Oled.print((5./1024)*random_value); // Print the Values  
  Oled.refreshDisplay();    // Update the Display 
 
  delay(500);
}