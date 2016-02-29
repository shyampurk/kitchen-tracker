#Procedure for calibrating the load cells


Step 1: Connect the Load Cells with the Arduino UNO as per the [Scematic](Schematic.png)
Step 2: Power up Arduino UNO and open the calibration [source code](hardware/bleHM10/calibrate.ino) in Arduino IDE
Step 3: Upload the program to the Arduino UNO
Step 4:	Open the Serial Monitor on the Arduino IDE
Step 5: Wait for sensor to calibrate and set initially to zero, then place a known weight of 1 KG on the both the sensors
Step 6: Check for the weight to be in pounds 
Step 7: If the weight does not matches with 2.2 lbs, change the calibration values on line 21 & 22 of calibration source code and upload the program to the Arduino UNO until the weight attains 2.2 lbs repeat [Step 3 to Step 7]
Step 8: Once the weight attains 2.2 lbs, note the calibration values, in the source code for both the sensor
Step 9: Update line 11 & 12 of BLE application [source code](hardware/bleHM10/bleHM10.ino) with the calibration values obtained in the previous step.
