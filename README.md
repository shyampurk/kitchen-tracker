# Kitchen Inventory Tracking

## Introduction

This is a model application to demonstrate how you can keep a track of your kitchen's inventory. By leveraging IoT, you can sense the weight of kitchen storage containers and hook them to the cloud which can enable smart decision making when it comes to tracking consumption patterns and getting timely alerts for replenishment and expiry.

## Setup

This application comprises of a hardware setup, a cloud hosted server application and a mobile app. 

The hardware is based on Linkit ONE , Arduino UNO and HM-10 BLE module. Two load cells are used to sense the weight of the containers. Refer [hardware build and install steps](HwBuildAndInstall.md) for setting up and programming the hardware.

The server application is hosted on [IBM Bluemix](http://www.ibm.com/cloud-computing/bluemix/). Refer this [link](Deploy.md) for instructions on how to deploy the server application on Bluemix.

The Mobile app is a cordova based android app used to track the inventory and provide some basic analytics. Refer this [link](AppBuild.md) for instructions on how to build the app.

This application relies on [PubNub](http://www.pubnub.com) data stream network for the underlying messaging between the hardware, the server and mobile app. Ensure that the same set of PubNub keys are used across all the components while configuring and building the application software.  

## Usage

Once the hardware and server is configured and deployed, the app can be launched to start tracking the inventory. But before launching the app, keep two containers on the load cell assembly and fill them up to a certain level with any commonly used kitchen consumable item, such as cereals or some form of staple food. 

### General Usage

Perform the following steps to use the app.

Step 1 - Once launched, the app screen will initially look like this.   
<img src="/imgs/Screenshot-0.jpg" align="center" width="250" >


Step 2 - Click on the settings icon on the top to bring up the settings page.     
<img src="/imgs/Screenshot-1.jpg" align="center" width="250" >

Step 3 - Enter a label text to identify the container, and choose a value for the 'Threshold' and 'Expiry in months' parameter from the slider, and then press submit. The threshold value is used to decide the minimum weight of the container. If the container weight is below this threshold, a visual indication is provided to the user to inform him about the critical level of inventory. Expiry is used to track the expiry of inventory item kept in this container.  

Step 4 - Perform the above steps for the second container by selecting container ID 002 at the top of settings screen.Once submitted,  you will get a message indicating that the container settings have been registered. Both containers have to be registered separately.

<img src="/imgs/Screenshot-2.jpg" align="center" width="250" >

Step 5 - Return back to the main screen and now you can see the container levels based on the current weight of the containers. Maximum weight supported by this application is 5 Kgs.

<img src="/imgs/Screenshot-3.jpg" align="center" width="250" >

Step 6 - In order to simulate the consumption of inventory, you can choose to take out some portions of the stored consumable from the container. Alternatively, you can also choose to refill the container. Either ways, you will notice that the app screen is updated with the new container weigh figures and visual level indicator.

Step 7 - If you want to reconfigure the container ( with a different label and/or threshold & expiry validity) , you can press the Reset button on the settings screen, after selecting the container ID. Once done, repeat step 3 to re-register the container with the new settings. Now you can return to the main screen and keep repeating step 6, to monitor the inventory status on the app. 


## Analytics

The mobile app provides basic analytics for the user to keep an eye on the daily consumption and replenishment patterns of the stored inventory.

Perform the following steps to access the analytics.

Step 1 - Click on History button below either of the container icon on the  main screen. This will bring up a history log of the consumption of replenishment data of the container for the last seven days.

<img src="/imgs/Screenshot-4.jpg" align="center" width="250" >


Step 2 - Click on Graph button below either of the container icon on the  main screen. This will bring up a chart which depicts the line graph of the consumption of replenishment pattern of the container for the last seven days. The blue line indicates replenishment and orange line indicates consumption.

<img src="/imgs/Screenshot-5.jpg" align="center" width="250" >


## Tracking Expiry

Since most of the kitchen consumables have an expiry date, this application can help track that and notify the user if the inventory has expired. 

Every time the containers are refilled, the expiry date is recalculated to be set on a future date, based on the container settings. The expiry value configured in the settings screen is for months.  So if the expiry value is set to 5, this means that the consumable stored in the container will expire 5 months from the the date when the setting is registered. If during this period the container is refilled again, the expiry is again recalculated from the date of refill and shifted in the future. 

In order to test the app for expiry notification, we can redeploy the server application by making a small config change which will treat the expiry value to be in minutes ( instead of months). This way we can set the inventory to expire within a few minutes and quickly verify the functionality of the app.

Perform the following steps to check for expiry.

Step 1 - Refer to the [deployment steps](Deploy.md). To set the expiry to be triggered in minutes, we have to redeploy the server application on Bluemix after changing the following configuration.

        - Under "Deploying the Application Server" section, refer to step 2
        - Modify the value of expiry to 1 in config.ini file
          - expiry = 1
        - Save the file and redeploy the application on Bluemix 
        
Step 2 - Once the server application starts running, perform the steps under "General Usage" section above to register the containers and their settings. Choose a value of 5 for the 'Expiry in months' parameter. Since we have now reconfigured the server to treat expiry in minutes, this will translate to an expiry of 5 minutes instead of 5 months.

Step 3 - Refill the containers with some content and wait for 5 minutes

Step 4 - After 5 minutes, take out some portion of the consumable from the container. The app screen will now display a expiry indication like this.

<img src="/imgs/Screenshot-6.jpg" align="center" width="250" >

Step 5 - In order to restore the app, Reset the containers and update the settings as per step 7 under "General Usage" section.

## Limitations
1. The expiry indication is displayed on the app only when the user consumes the inventory after to the  expiry period is crossed.
2. The app does not retain the container settings for both containers during subsequent settings display. 
3. After every consumption or refill, the hardware may take atleast 20 to 30 seconds to stabilize the weight and send the new weight value to server.




