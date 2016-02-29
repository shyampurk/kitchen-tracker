***************************
#KITCHEN INVENTORY TRACKER 
***************************

##Steps to Build the Project 
---------------------------

##Hardware Requirements:
-----------------------
The list of hardware components if this project is as follows

	-	Arduino UNO
	-	Load Cells
	-	HX711 Load Cell Amplifier 
	-	HM - 10 BLE Module
	-	Mediatek Linkit One HDK

Refer to the [schematic diagram](Schematic.png) for teh hardware setup

##Software Requirements :
The following software and driver packages need to be installed in the build system. 

	- 	OS : Windows 7/8 or OSX. ( The steps provided below are for Windows 7. Linkit ONE officially supports Windows & MAC Operating Systems only)
	- 	Arduino IDE
	- 	LinkIt One SDK
	- 	USB COM Port Driver
	- 	USB to Serial Driver  

##Installation of the Software/Drivers

### Prerequisites
1. Before proceeding with the software installation, make sure to disable driver signing check on Windows 7 to allow third party drivers ( non Microsoft) to be installed. This option is available as part of advanced boot option which can be brought up during windows 7 boot time by pressing F8 key ( Shift Key for Windows 8)
2. Disable Automatic Driver Installation on Windows OS. The automatic download and installation of device drivers can prevent proper installation of the LinkIt ONE USB COM port driver on Windows 7 machines. If you’ve already disabled the automatic installation of device drivers, you can skip this step, otherwise:

	- Open Control Panel and search for and open Change device installation settings.
	- In Device Installation Settings select "No, let me choose what to do" option, then click "Never install driver software from Windows Update". 
	- Also make sure to uncheck "Automatically get the device application and information provided by your device manufacturer".
	- Click "Save Changes" and exit the control panel.
	 

###Install Arduino IDE & Drivers
----------------------------------------------------
Step 1: Setup the Arduino IDE to Program the Arduino UNO and Linkit One

Installing the Arduino IDE SDK

	- 	Download the Arduino IDE 1.6.6 [Recommeded for LINKIT]
		
			The Arduino IDE provides your coding environment and is used for monitoring the 
		development board. The LinkIt ONE SDK is compatible with Arduino IDE version 1.6.6.

			[https://www.arduino.cc/en/Main/OldSoftwareReleases#previous]


Step 2: Download the USB COM port driver for the LinkIt ONE Development Board

	- 	A USB COM port driver is required for the LinkIt ONE SDK installation, get it here.

			[download.labs.mediatek.com/mediatek_linkit_windows-com-port-driver.zip]


		1.	Extract the content of the USB COM port driver zip file you downloaded.
	    	2.	Run the installer InstallMTKUSBCOMPortDriver.exe and follow the instructions.

Step 3 : Download and install Windows USB to Serial driver by downloading and unzipping the [package](tools/CP210x_Windows_Drivers.zip) and running CP210xVCPInstaller_x64.exe or CP210xVCPInstaller_x86.exe ( for 64 bit or 32 bit OS ) installer binary.


You now have all the hardware and software you need to get started.

    -	Start Arduino and open Preferences window.
    -	Enter http://download.labs.mediatek.com/package_mtk_linkit_index.json into Additional Board 
    	Manager URLs field. 
    -	You can add multiple URLs, separating them with commas.
    -	Open Boards Manager from Tools > Boards > Board Manager and install Linkit One SDK
    -	Make sure you have installed the boards by finding linkit on Tools > Boards > LinkitOne

PREREQUISITE:
--------------

Step 1: Update the Firmware for the HM-10 BLE Moulde by following link

			https://suryaigor.wordpress.com/2016/02/05/upgrading-firmware-to-hm-10-cc2541-ble-4-0/

Step 2:	Make sure you have connected WiFi/Bluetooth Antenna to the Linkit One Board

UPGRADING LINKIT ONE:
---------------------




Sensor-Controller Build 
-------------------------

	-	Follow the schematic and build the circuit with the LOAD CELL, Amplifier and Arduino UNO 
	- 	GIT CLONE the Github Repo form following link
	-	Open the (git_repo)/hardware/bleHM10/bleHM10.ino using Arduino IDE
	-	Select Tools > Boards > Arduino UNO
	-	Select the COM Port at Tools > Port > (COM PORT)
	- 	Compile and Upload the code to the Arduino IDE

Linkit-PubNub Build
--------------------

	-	Open the (git_repo)/linkitble/pubnub_linkit/pubnub_linkit.ino using Arduino IDE
	-	Open the (git_repo)/linkitble/pubnub_linkit/settings.h
	- 	Modify with your Pubnub KEYS, local WIFI Router SSID and PASSWORD
	-	Select Tools > Boards > Linkit One
	-	Check for the debug port on the Device Manager > COM Ports > COMxx(DEBUG)
	-	To Uplod the Script, select the DEBUG COM Port at Tools > Port > (COMxx PORT)
	- 	Compile and Upload the code to the Arduino IDE by clicking the upload button.
	
