// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("Starting...");
}

void loop() {
  if (Serial.available()) {
    delay(100);  //wait some time for the data to fully be read
    lcd.clear();
    int wordNum = 0;
    while (Serial.available() > 0) {
      char c = Serial.read();
      if (c == '\n') {
          break;
      }
      else if (c >= 'A' && c <= 'Z') {
        lcd.clear();
      }
      lcd.write(c);
    }
  }
}
