# Kitchen Inventory Tracking

## Introduction

This is a model application to demonstrate how you can keep a track of your kitchen's inventory. By leveraging IoT, you can sense the weight of kitchen storage containers and hook them to the cloud which can enable smart decision making when it comes to tracking consmuption patterns and getting timely alerts for replenishment and expiry.

## Setup

This application comprises of a hardware setup, a cloud hosted server application and a mobile app. 

The hardware is based on Linkit ONE and HM-10 BLE module. two load cells are used to sense the weight of the containers. Refer this [link](HwBuildAndInstall.md) for setting up and programming the hardware.

The server application is hosted on IBM Bluemix. Refer this [link](Deploy.md) for instructions on how to deploy the server application on Bluemix.

The Mobile app is a cordova based android app used to track the inventory and provide some basic analytics. Refer this [link](AppBuild.md) for instructions on how to build th app.

This application relies on PubNub data stream network for the underlying messaging between the hardware, the server and app. Ensure that the same set of PubNub keys are used across all the components while configuring and building the application software.  

## Usage

Once the hardware and server is configured and deployed, the app can be launched to start tracking the inventory. But before launching the app, keep two containers on the load cell assembly and fill them up to a certain level with any commonly used kitchen consumable item, such as cereals (rice, wheat, etc.) or staples. 

### General Usage

Perform the following steps to use the app.

Step 1 - Once launched, the app screen will initially look like this.   
<img src="/imgs/Screenshot-0.jpg" align="center" width="250" >


Step 2 - Click on the settings icon on the top to bring up the settings page.     
<img src="/imgs/Screenshot-1.jpg" align="center" width="250" >

Step 3 - Enter a label text to identify the container, and choose a value for the threshold and expiry date and then press submit. The threshold value is used to decide the minimum weight of the container. If the container weight is below this threshold, a visual indication is provided to the user to inform him about the depleting inventory. Expiry date is in months. This is used to track the expiry of inventory item kept in this container.  

Step 4 - Perform the above steps for the second container by selecting container ID 002 at the top of settings screen.Once submitted,  you will get a message indicating that the container settings have been registered. 

<img src="/imgs/Screenshot-2.jpg" align="center" width="250" >

Step 5 - Return back to the main screen and now you can see the container levels based on the current weight of the containers.

<img src="/imgs/Screenshot-3.jpg" align="center" width="250" >

Step 6 - In order to simulate the consumption of inventory, you can choose to take out some portions of the stored consumable from the container. Alternatively, you can also choose to refill the container. Either ways, you will notice that the app screen is updated with the new container weigh figures and visual level indicator.

Step 7 - If you want to reconfigure the container ( with a different label and/or threshold & expiry validity) , you can press the Reset button on the settings screen, after selecting the container ID. Once done, repeat step 3 to re-register the container with the new settings. Now you can return to the main screen and keep repeating step 6, to monitor the inventory status on the app. 


## Analytics

The mobile app provides basic analytics for the user to keep an eye on the daily consumption and replenishment patterns of the stored inventory.

Perform the following steps to access the analytics.

Step 1 - Click on History button below either of the container icon on the  main screen. This will bring up a history log of the consumption of replenishment data of the container for the last seven days.

<img src="/imgs/Screenshot-4.jpg" align="center" width="250" >


Step 2 - Click on Graph button below either of the container icon on the  main screen. This will bring up a chart which depicts the line graph of the consumption of replenishment pattern of the container for the last seven days.

<img src="/imgs/Screenshot-5.jpg" align="center" width="250" >


