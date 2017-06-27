# Deployment on IBM Bluemix

## Prerequisites

    - You should have a valid IBM account
    - You should have a Bluemix subscription and access to your Bluemix dashboard with atleast one space created
    - You should have the cloudfoundry command line tool installed
    (https://github.com/cloudfoundry/cli/releases)
    - You should have a PubNub subscription

## Deploying DashDB Service

### Step 1: 
Login to Bluemix with your credentials.

### Step 2: 
In your dashboard, goto Catalog and select the Data and Analytics Section
			
	You can see that the dashDB service will be listed under this section or you can search for dashDB 

### Step 3: 
Click on dashDB service icon and create a dashDB service instance for your space ,
		
	Service name - Enter a name for the service of your choice
	Selected Plan - Choose 'Entry'.

Click CREATE to create the dashdb service instance.

### Step 4: 
After creation of the service, go back to dashboard.Now you can see the dashDB service added to your space. Click the service and select <strong>Service Credential</strong> in the side menu.

### Step 4.1: 
Click New Credential button to create service credential for the instance and copy the generated credentials to any file.

	Credential name - Enter a name for the Credential of your choice

You can see your dashDB Host name,Database name,user id and password.

    	Make a note of Host Name, Port Number , Database Name, User ID and Password.

### Step 5: 
Now select <strong>Manage</strong> option in side menu and click the <strong>Open</strong> button , You can see your newly created dashDB service home page.

### Step 6: 
In the Side Main Menu click <strong>Tables</strong>,Here you can create the table for this application.

Click <strong>'Add Table'</strong> to create the table for kitchen tracking application by entering the below SQL stamement in the bottom text area.
		
    CREATE TABLE "KITCHENTRACKERAPP" 
    (
      "SCALE_ID" VARCHAR(3),
      "DATES" DATE,
      "TIME" VARCHAR(10),
      "QUANTITY" FLOAT,
      "STATUS" INT 
    );



### Step 7: 
Then click the button <strong>"Run DDL"</strong>.

You can see the newly created table by selecting your schema and table name. Your schema is same as your username as displayed in the generated Service Credential.


## Deploying the Application Server

### Step 1 : 
Clone this github repository

### Step 2 : 
Update the parameters in the [config.ini](kitchen_tracker/config.ini)

	pub_key = PubNub Publish Key
	sub_key = PubNub Subscribe Key
	db_schema = User ID of the DashDB instance , in caps
	db_name = Database name
	db_host = Host Name
	table_name = Table name is set to KITCHENTRACKERAPP
	username = User ID of the DashDB instance
	pwd = Password of dashDB instance
	port = Port Number
	expiry = 0 ( Leave it to default value of zero)
	

### Step 3 : 
Open the [manifest file](https://github.com/shyampurk/kitchen-tracker/blob/master/kitchen_tracker/manifest.yml) and update the follwing entries

		applications:
			- name : <name of the application on server>
	
		services
			- <dashdb instance name>

		where 
			<name of the application on server> - Any desired name for the application
			<dashdb instance name> - name of the dashdb service instance that you have created in the previous section.


### Step 4 : 
Login to Bluemix console via <strong>cf</strong> tool and select the space.

### Step 5 : 
Change directory to the server application root (kitchen_tracker) under the cloned github repository.

### Step 6 : 
Run the following command to push the application code to bluemix

		'cf push' 

Once successfully pushed, the server application will be automatically started. You can check its state in your bluemix dashboard and see that its state is set to 'Running'
