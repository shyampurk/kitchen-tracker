# Deployment on IBM Bluemix

##Prerequisites

    - You should have a valid IBM account
    - You should have a Bluemix subscription and access to your BLuemix dashboard with atleast one space created
    - You should have the cloudfoundry command line tool installed
    (https://github.com/cloudfoundry/cli/releases)
    - You should have a PubNub subscription

## Deploying DashDB Service

Step 1: Login to Bluemix with your credentials.

Step 2: In your dashboard, goto Catalog and select the Data and Analytics Section
			
			You can see that thedashDB service will be listed under this section or you can search for dashDB 

Step 3: Create a service for your space by filling following details,
		
			1) Space - Your space name where you want to add this service ( This might have been preselected if you have an existing space)
    		2) App   - You can select "leave unbound"
			3) Service name - Enter a name for the service of your choice
			4) Credential name - Enter a name for the Credential of your choice
			5) Selected Plan - Depends on the data you can select your plan but for up to 1 GB No charge.
			6) Click CREATE to create the dashdb service instance.

Step 4: After creation of the service, go back to dashboard 
		You can see the dashDB service added to your space, click the service and click the launch button and you can see the dashDB home page.

Step 5: In the Side Menu under the Connect -> Connection information, 
		
	You can see your dashDB Host name,Database name,user id,pwd.

        Make a note of Host Name, Port Number , Database Name, User ID and Password.

Step 6: In the Side Main Menu click Tables,Here you can create the table for this application.
		Click Add Table to create the table for kitchen tracking application by entering the below SQL stamement in the bottom text area.
		
    CREATE TABLE "KITCHENTRACKERAPP" 
    (
      "SCALE_ID" VARCHAR(3),
      "DATES" DATE,
      "TIME" VARCHAR(10),
      "QUANTITY" FLOAT,
      "STATUS" INT 
    );



Step 7: Then click the button "Run DDL".
		You can see the newly created table by selecting your schema and table name. Your schema is same as your username as displayed in Connect > Connection Information menu.


## Deploying the Application Server

Step 1 - Clone this github repository

Step 2 - Update the parameters in the [config.ini](kitchen_tracker/config.ini)

	pub_key = PubNub Publish Key
	sub_key = PubNub Subscribe Key
	db_schema = User ID of the DashDB instance , in caps
	db_name = Database name
	db_host = Host Name
	table_name = Table name is set to KITCHENTRACKERAPP
	username = User ID of the DashDB instance
	pwd = Password of dashDB instance
	port = Port Number
	

Step 3 - Open the manifest file and update the follwing entries

		applicationa:
			- name : <name of the application on server>
	
		services
			- <dashdb instance name>

		where 
			<name of the application on server> - Any desired name for the application
			<dashdb instance name> - name of the dashdb service instance that you have created in the previous section.


Step 4 - Login to Bluemix console via cf tool and select the space.

Step 5 - Change directory to the server application root (kitchen-tracker) under the cloned github repository.

Step 6 - Run the following command to push the application code 

		'cf push' 

