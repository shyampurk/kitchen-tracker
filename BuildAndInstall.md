***************************
#KITCHEN INVENTORY TRACKER 
***************************

##Steps to Build the Project 
---------------------------

##Hardware Requirements:
-----------------------
The list of hardware components for this project are as follows

	-	Arduino UNO board
	-	YXC-133 Load Cell (2 nos)
	-	HX711 Load Cell Amplifier 
	-	HM - 10 BLE Module
	-	Mediatek Linkit One HDK

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
1. Before proceeding with the software installation, make sure to disable driver signing check on Windows 7 to allow third party drivers ( non Microsoft) to be installed. 

##For Windows 7 
	
	- This option is available as part of advanced boot option which can be brought up during windows 7 boot time by pressing F8 key
	
##For Windows 8/8.1/10

	- Hold down the Windows key on your keyboard and press the letter C to open the Charm menu, then click the gear icon (Settings).
	- Click More PC Settings -> Click General -> Under Advanced Startup, click Restart Now.

NOTE: In Windows 8.1, the ‘Restart Now’ button has moved to ‘PC Setting -> Update & Recovery -> Recovery.

	- After restarting, click Troubleshoot -> Click Advanced Options -> Click Windows Startup Settings -> Click Restart
	- After restarting your computer a second time, choose Disable driver signature enforcement from the list by typing the number 7 on your keyboard.Your computer will restart automatically.
	
2. Disable Automatic Driver Installation on Windows OS. The automatic download and installation of device drivers can prevent proper installation of the LinkIt ONE USB COM port driver on Windows 7 machines. If you’ve already disabled the automatic installation of device drivers, you can skip this step, otherwise:

	- Open Control Panel and search for and open "Change Device Installation Settings" dialog box.
	- In the dialog box, select "No, let me choose what to do" option, then click "Never install driver software from Windows Update" option. 
	- Also if visible under Windows 7/8/10, make sure to uncheck "Automatically get the device application and information provided by your device manufacturer" option.
	- Click "Save Changes" to save the settings and exit the "Change Device Installation Settings" dialog box and the control panel.
	 

###Install Arduino IDE & Drivers
----------------------------------------------------
Step 1: Setup the Arduino IDE to Program the Arduino UNO and Linkit One

Installing the Arduino IDE SDK

	- 	Download the Arduino IDE 1.6.6 [Recommeded for LINKIT]
		
			The Arduino IDE provides your coding environment and is used for monitoring the 
		development board. Currently, the LinkIt ONE SDK is compatible with Arduino IDE version 1.6.6.

			[https://www.arduino.cc/en/Main/OldSoftwareReleases#previous]


Step 2: Download the USB COM port driver for the LinkIt ONE Development Board

	- 	A USB COM port driver is required for the LinkIt ONE SDK installation, get it here.

			[download.labs.mediatek.com/mediatek_linkit_windows-com-port-driver.zip]


		1.	Extract the content of the USB COM port driver zip file you downloaded.
	    	2.	Run the installer InstallMTKUSBCOMPortDriver.exe and follow the instructions.

Step 3 : Download and install Windows USB to Serial driver by downloading and unzipping this [package](tools/CP210x_Windows_Drivers.zip) and running CP210xVCPInstaller_x64.exe or CP210xVCPInstaller_x86.exe ( for 64 bit or 32 bit OS ) installer binary.


##Installation of Linkit ONE SDK on Arduino IDE
Once all the requisite softwares and drivers are installed , you can configure Arduino IDE to install Linkit ONE SDK by following the steps below.

    -	Start Arduino IDE and open File > Preferences window.
    -	Under teh Settings tab, enter http://download.labs.mediatek.com/package_mtk_linkit_index.json into Additional Board 
    	Manager URLs field. 
    -	Open Boards Manager from Tools > Boards > Board Manager. This will open the "Boards Manager" window
    -	On the "Boards Manager" window, scroll down and search for LinkIt ONE entry. Select it and click on install button.
    -	Wait for the Link IT ONE SDK to be downloaded. This may take some time.
    -	Once installed, make sure you have emabled the LinkIt ONE board by selecting "LinkIt ONE" from Tools > Boards menu.


##Build Procedure for Hardware Components

### Firmware update for HM-10 BLE Module

Step 1: Update the Firmware for the HM-10 BLE Moulde by following link. Before performing the update, you also have connect the BLE module hardware to FTDI breakout board.   

			https://suryaigor.wordpress.com/2016/02/05/upgrading-firmware-to-hm-10-cc2541-ble-4-0/
	
	


### Upgrade and Build Application Software:
--------------------------------

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
	-	Open the application [source code](linkitble/pubnub_linkit/pubnub_linkit.ino) using Arduino IDE
	-	Open the [config header file](linkitble/pubnub_linkit/settings.h) and update your pubnub keys (pubkey and subkey), local WIFI Router SSID, password and auth type (WIFI_AP , WIFI_PASSWORD , WIFI_AUTH).
	-	Select Tools > Boards > Linkit One
	-	Check for the debug port on the Control Panel's Device Manager > COM Ports > COMxx(DEBUG)
	-	To Uplod the code, select the DEBUG COM Port at Tools > Port > (COMxx PORT)
	- 	Compile the code under Arduino IDE and Upload to LinkIt ONE by clicking the upload button.
	

#### Build & Install application software on Arduino Uno
-------------------------

	-	Install the [HX711](library/HX711.zip) library in Adruino IDE
	-	Open the application [source code](/hardware/bleHM10/bleHM10.ino) using Arduino IDE
	-	Select Tools > Boards > Arduino UNO
	-	Select the COM Port ( the USB port mapped COM port to which the Arduino Uno is connected )  at Tools > Port > (COM PORT)
	- 	Compile the code under Arduino IDE and Upload to Arduino Uno
	


