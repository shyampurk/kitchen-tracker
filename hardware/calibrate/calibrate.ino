
/*******************************************************************************************************
 *                                        SMART KITCHEN TRACKER                                        *
 *******************************************************************************************************/
#include "HX711.h"

//Pins for the Load Cell 1
#define DOUT   4
#define CLK    2
//Pins for the Load Cell 2
#define DOUT1  5
#define CLK1   3


//Initialize the load cell
HX711 scale(DOUT, CLK);
HX711 scale1(DOUT1, CLK1);

//Setting up the Calibration factor for the load cells
//Change these values by adding/subtracting to calibrate the sensor 
#define calibration_factor -395050
#define calibration_factor1 -347429

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 calibration sketch");
  //Reset the scale to 0
  scale1.set_scale(calibration_factor); 
  scale.set_scale(calibration_factor1);
  scale1.tare();
  scale.tare();
  //Get a baseline reading
  long zero_factor_1 = scale.read_average(); 
  long zero_factor_2 = scale1.read_average(); 
  Serial.print("Zero factor for Sensor 1: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor_1);
  Serial.print("Zero factor for Sensor 2: "); //This can be used to remove the need to tare the scale. Useful in permanent scale projects.
  Serial.println(zero_factor_2);
}

void loop() {
  //Adjust to this calibration factor
  scale1.set_scale(calibration_factor); 
  scale.set_scale(calibration_factor1);

  Serial.print("Reading for Sensor 1: ");
  Serial.print(scale.get_units(), 3);
  Serial.print(" lbs"); 
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();
  Serial.println();
  Serial.println();
  Serial.print("Reading for Sensor 2: ");
  Serial.print(scale1.get_units(), 3);
  Serial.print(" lbs"); 
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor1);
  Serial.println();
  Serial.println();
  Serial.println();
  delay(1000);
}

