/*******************************************************************************************************
 *                                        SMART KITCHEN TRACKER                                        *
 *******************************************************************************************************/
//Importing the Software Serial and Load Cell HX711 Amplifier Library 
#include <SoftwareSerial.h>
#include "HX711.h"

//Setting up the Serial Communication between the HM-10 BLE and Controller
SoftwareSerial Serial4(11,10);  //Tx,Rx
//Setting up the Calibration factor for the load cells
#define calibration_factor -395050
#define calibration_factor1 -347429
//Pins for the Load Cell 1
#define DOUT   4
#define CLK    2
//Pins for the Load Cell 2
#define DOUT1  5
#define CLK1   3

//Initialize the load cell
HX711 scale(DOUT, CLK);
HX711 scale1(DOUT1, CLK1);
/*******************************************************************************************************
 Function Name            : setup
 Description              : Initialize the Bluetooth and Connection WiFi to the local AP
                            and scanning the available bluetooth connections
 Parameters               : None
 *******************************************************************************************************/
void setup() {
  //Begin the BLE Connection with 9600 BAUD
  Serial4.begin(9600);
  Serial.begin(9600);
  //Initalize the calibration factor for the load cells 
  scale1.set_scale(calibration_factor); 
  scale.set_scale(calibration_factor1);
  scale1.tare();
  scale.tare(); 
}

/*******************************************************************************************************
 Function Name            : loop
 Description              : Gets the weight from  load cells and push to likit via ble
 Parameters               : None
 *******************************************************************************************************/
void loop() {
  float l_weight_loadCell_1,l_weight_loadCell_2;
  l_weight_loadCell_1 = dataOne();
  l_weight_loadCell_2 = dataTwo();
  //Forms a JSON data
  String cmd = "[\"";
  cmd += String(l_weight_loadCell_1);
  cmd += "\",\"";
  cmd += String(l_weight_loadCell_2);
  cmd += "\"]";
  //Push the data from HM-10 to the Linkit BLE
  Serial.println(cmd);
  Serial4.println(cmd);
  delay(1000);
}
/*******************************************************************************************************
 Function Name            : dataOne
 Description              : Obtains the present weight from the load cell 1
 Parameters               : None
 return                   : float - weight obtained
 *******************************************************************************************************/
float dataOne(){
  char l_buf[50];
  //Converts the weight from pound to kgs
  float l_weight_in_kgs_0 = scale.get_units()  * 0.453592;
  if(l_weight_in_kgs_0 >= 0.01){
    l_weight_in_kgs_0 = l_weight_in_kgs_0 - 0.14;
    return l_weight_in_kgs_0;
  }
  else{
    return 0;
  }
}
/*******************************************************************************************************
 Function Name            : dataTwo
 Description              : Obtains the present weight from the load cell 2
 Parameters               : None
 return                   : float - weight obtained
 *******************************************************************************************************/
float dataTwo(){
  char l_buf[50];
  //Converts the weight from pound to kgs
  float l_weight_in_kgs_1 = scale1.get_units() * 0.453592;
  if(l_weight_in_kgs_1 >= 0.01){
    l_weight_in_kgs_1 = l_weight_in_kgs_1 + 0.12;  
    return l_weight_in_kgs_1;
  }
  else{
    return 0;
  }
}
//End of the Program
/************************************************************************************************************************/
