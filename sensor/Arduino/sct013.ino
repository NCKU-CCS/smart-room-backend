#include "EmonLib.h"
// Include Emon Library

EnergyMonitor emon1;
// Create an instance

void setup() {
  Serial.begin(9600);
  // Current: input pin, calibration.
  emon1.current(1, 65);
}

void loop() {
  // Calculate Irms only
  double Irms = emon1.calcIrms(1480);
  // Apparent power
  Serial.print(Irms);
  Serial.print(" ");
  Serial.println(Irms*220.0);
  // delay for one minute
  delay(60000);
}
