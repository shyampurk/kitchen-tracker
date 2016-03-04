
#KITCHEN INVENTORY TRACKER 

##Steps for building the project hardware 
---------------------------

##Hardware Requirements:

The list of hardware components for this project are as follows

	-	Arduino UNO board
	-	YXC-133 Load Cell (2 nos)
	-	HX711 Load Cell Amplifier 
	-	HM - 10 BLE Module ( along with FTDI breakout board, for firmware upgrade only)
	-	Mediatek Linkit One HDK
	-	FTDI USB to Serial Converter Module

Refer to the [schematic diagram](Schematic.png) for the hardware setup and pin connections

##Software Requirements :
The following software and driver packages need to be installed in the build system. 

	- 	OS : Windows 7/8 or OSX. ( The steps provided below are for Windows 7. Linkit ONE officially supports Windows & MAC Operating Systems only)
	- 	Arduino IDE
	- 	LinkIt One SDK
	- 	USB COM Port Driver
	- 	USB to Serial Driver  


##Installation of the Software/Drivers

### Prerequisites
Step 1: Before proceeding with the software installation, make sure to disable driver signing check on Windows 7 to allow third party drivers ( non Microsoft) to be installed. 

		For Windows 7 
	
		- This option is available as part of advanced boot option which can be brought up during windows 7 boot time by pressing F8 key
	
		For Windows 8/8.1/10

		- Hold down the Windows key on your keyboard and press the letter C to open the Charm menu, then click the gear icon (Settings).
		- Click More PC Settings -> Click General -> Under Advanced Startup, click Restart Now.

		NOTE: In Windows 8.1, the ‘Restart Now’ button has moved to ‘PC Setting -> Update & Recovery -> Recovery.

		- After restarting, click Troubleshoot -> Click Advanced Options -> Click Windows Startup Settings -> Click Restart
		- After restarting your computer a second time, choose Disable driver signature enforcement from the list by typing the number 7 on your keyboard.Your computer will restart automatically.
	
Step 2: Once you disable Automatic Driver Installation on Windows OS. The automatic download and installation of device drivers can prevent proper installation of the LinkIt ONE USB COM port driver on Windows 7 machines. If you’ve already disabled the automatic installation of device drivers, you can skip this step, otherwise:

	- Open Control Panel and search for and open "Change Device Installation Settings" dialog box.
	- In the dialog box, select "No, let me choose what to do" option, then click "Never install driver software from Windows Update" option. 
	- Also if visible under Windows 7/8/10, make sure to uncheck "Automatically get the device application and information provided by your device manufacturer" option.
	- Click "Save Changes" to save the settings and exit the "Change Device Installation Settings" dialog box and the control panel.
	 

###Install Arduino IDE & Drivers
----------------------------------------------------
Step 1: Setup the Arduino IDE to Program the Arduino UNO and Linkit One

The Arduino IDE provides your coding environment and is used for monitoring the development board. Currently, the LinkIt ONE SDK is compatible with Arduino IDE version 1.6.6 [Recommeded for LINKIT]. Download Arduino IDE from this [Link](https://www.arduino.cc/en/Main/OldSoftwareReleases#previous)


Step 2: Download the USB COM port driver for the LinkIt ONE Development Board

USB COM port driver is required for the LinkIt ONE SDK installation. It can be downloaded from this [Link](http://download.labs.mediatek.com/mediatek_linkit_windows-com-port-driver.zip)

		1.	Extract the content of the USB COM port driver zip file you downloaded.
		2.	Run the installer InstallMTKUSBCOMPortDriver.exe and follow the instructions.

Step 3 : Download and install Windows USB to Serial driver by downloading and unzipping this [package](tools/CP210x_Windows_Drivers.zip) and running CP210xVCPInstaller_x64.exe or CP210xVCPInstaller_x86.exe ( for 64 bit or 32 bit OS ) installer binary.


##Installation of Linkit ONE SDK on Arduino IDE
Once all the requisite softwares and drivers are installed , you can configure Arduino IDE to install Linkit ONE SDK by following the steps below.

    -	Start Arduino IDE and open File > Preferences window.
    -	Under the Settings tab, enter the string (without quotes) "http://download.labs.mediatek.com/package_mtk_linkit_index.json" into Additional Board Manager URLs field. 
    -	Open Boards Manager from Tools > Boards > Board Manager. This will open the "Boards Manager" window
    -	On the "Boards Manager" window, scroll down and search for LinkIt ONE entry. Select it and click on install button.
    -	Wait for the Link IT ONE SDK to be downloaded and installed under the Arduino IDE. This may take some time.
    -	Once installed, make sure you have emabled the LinkIt ONE board by selecting "LinkIt ONE" from Tools > Boards menu.


##Build Procedure for Hardware Components

### Firmware update for HM-10 BLE Module

Step 1 : Extract the firmware and tools from this [package](tools/BLE_HM10_FirmwareTool.rar)

	- This package containes the following files
        	-- HMComAssistant.exe
	   		-- HMSoft.exe
	 		-- HMSoft.bin

Step 2 : For performing the firmware update, the BLE module hardware has to be connected to FTDI breakout board. Setup the Connection with HM-10 Module and FTDI Chip as follows

	- Connect the HM-10 CC2541 BLE module to the FTDI Breakout Board as shown in the [schematic](FTDIandHM-10.png)
	- Check the COM Port of the FTDI board connected to the PC on Device Manager
	- If COM Port is not detected, upgrade the drivers using following link [FTDI Driver Link](http://www.ftdichip.com/Drivers/D2XX.htm). 
	    

Step 3 : Connect to HM-10 BLE module and set it up for firmware update as follows

		- Launch the HMComAssistant.exe form the downloaded folder on your PC
		- Select the COM Port on the HMComAssistant
		- On HMComAssistant click Open Port
		- Enter AT command on the text box and Click SEND button
		- If HM-10 responds with OK then module connection is made correctly, if not check the connections made.
		- To pull the module to upgrading mode, Send AT+SBLUP commad.
		- If module responds with OK+SBLUP, then we are ready to upgrade the firmware.

Step 4 : Update firmware as follows

		- Launch the HMSoft.exe executable file on the downloaded folder
		- Select the firmware image from the downloaded folder [HMSoft.bin]
		- Enter the right COM Port number on COM Port
		- Click on Load Image button to start burning the firmware to the HM-10 BLE module
		- Wait for the pop-up Download Completed Successfully

### Upgrade and Build Application Software:

#### Prerequisites

Step 1 : Clone this repository into the build system.

Step 2 : Sign up for [PubNub](www.pubnub.com) subscription and get your PubNub publish and subscribe keys

Step 3 : Make sure you have connected WiFi/Bluetooth Antenna to the Linkit One Board

Step 4 : Follow the [schematic diagram](Schematic.png) and build the circuit.

Step 5 : Power up the LinkIt ONE and Arduino Uno board through the USB port on the build system. 

#### Build & Install application software on LinkIt ONE

Step 1 - Update the Firmware for the Linkit One by following this official link

	http://labs.mediatek.com/site/global/developer_tools/mediatek_linkit/get-started/windows_os_stream/update_firmware/index.gsp

Step 2 : Perform the following steps to build and load the the application on LinkIt ONE 

- Open the application [source code](linkitble/pubnub_linkit/pubnub_linkit.ino) using Arduino IDE
- Open the [config header file](linkitble/pubnub_linkit/settings.h) and update your pubnub keys (pubkey and subkey), local WIFI Router SSID, password and auth type (WIFI_AP , WIFI_PASSWORD , WIFI_AUTH).
- Select Tools > Boards > Linkit One
- Check for the debug port on the Windows Control Panel's Device Manager > COM Ports > COMxx(DEBUG)
- To Upload the code, select the DEBUG COM Port at Tools > Port > (COMxx PORT)
- Compile the code under Arduino IDE and Upload to LinkIt ONE by clicking the upload button.
	

#### Build & Install application software on Arduino Uno

Before installing the application software on Arduino UNO, calibration of the load cells must be performed to sense the weight accurately. Perform the [calibration steps](Calibrate.md) to calibrate the load cells and then proceed as below

Step 1 : Install the [HX711](library/HX711.zip) library in Adruino IDE

Step 2 : Open the application [source code](/hardware/bleHM10/bleHM10.ino) using Arduino IDE

Step 3 : Select Tools > Boards > Arduino UNO

Step 4 : Select the COM Port ( the USB port mapped COM port to which the Arduino Uno is connected )  at Tools > Port > (COM PORT)

Step 5 : Compile the code under Arduino IDE and Upload to Arduino Uno
	


