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

Once the hardware and server is configured and deployed, the app can be launched to start tracking the inventory. Perform the following steps to use the app.

Step 1 - Once launched, the app screen will initially look like this.   
<img src="/imgs/Screenshot-0.jpg" align="center" width="250" >


Step 2 - Click on the settings icon on the top to bring up the settings page.     
<img src="/imgs/Screenshot-1.jpg" align="center" width="250" >

Step 3 - Enter a label text to identify the container, and choose a value for the threshold and expiry date and then press submit. The threshold value is used to decide the minimum weight of the container. If the container weight is below this threshold, a visual indication is provided to the user to inform him about the depleting inventory. Expiry date is in months. This is used to track the expiry of inventory item kept in this container.  

Step 4 - Perform the above steps for the second container. You will get a message indicating that the container settings have been registered. <img src="/imgs/Screenshot-2.jpg" align="center" width="250" >

Step 5 - Return back to the main screen and now you can see the container levels based on the weights.
<img src="/imgs/Screenshot-3.jpg" align="center" width="250" >



