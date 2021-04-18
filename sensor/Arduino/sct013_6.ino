// Include Emon Library
#include "EmonLib.h"

#define emon_num 6
#define calibration 60

// Create instance
EnergyMonitor emon_array[emon_num];

void setup() {
  Serial.begin(9600);
  // Current: input pin, calibration.
  for (int i=0 ; i < emon_num; i++)
    emon_array[i].current(i, calibration);
}

void loop() {
  // Calculate Irms only
  double Irms = 0;
  for (int i = 0 ; i < emon_num ; i++)
  {
    Irms = emon_array[i].calcIrms(1480);
    Serial.print(Irms);
    Serial.print(",");
  }
  Serial.println();
  // delay for one minute
  delay(60000);
}
