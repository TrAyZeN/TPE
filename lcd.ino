// include the library code:
#include <LiquidCrystal.h>
 
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12,11,5,4,3,2);
 
void setup() {
  Serial.begin(115200);
  lcd.begin(16, 2);
  lcd.print("Demarrage...");
}
 
void loop() {
  if (Serial.available()) {
    delay(100);  //wait some time for the data to fully be read
    lcd.clear();
    while (Serial.available() > 0) {
      char c = Serial.read();
      if (c == "erase") {
        lcd.clear(); //not working actually, i need to fix this
      }
      else{
        lcd.write(c);
      }
    }
  }
}
