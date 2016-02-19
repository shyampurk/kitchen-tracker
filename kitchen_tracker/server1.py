'''*********************************************************************************
SERVER - KITCHEN TRACKER
*********************************************************************************'''
#Import the Modules Required
from pubnub import Pubnub
import datetime
from dateutil.relativedelta import relativedelta
import ConfigParser
import logging

# Modules for the dashDB
import ibmdbpy
from ibmdbpy.base import IdaDataBase
from ibmdbpy.frame import IdaDataFrame
from pandas import DataFrame
import pandas

#Importing the Config File and Parsing the file using the ConfigParser
config_file = "./config.ini"
Config = ConfigParser.ConfigParser()
Config.read(config_file)
logging.basicConfig(filename='logger.log',level=logging.DEBUG)
#CONSTANTS 
TIMESPAN_FOR_HISTORY = 7

#DATA STRUCTURES
#KEY = ContainerID VALE =  Label,Expiry in Months, Critical Level, End Date 
g_containerSettings = dict()
SETTINGS_LABEL = 0
SETTINGS_EXPIRY = 1
SETTINGS_CRITICAL_LEVEL = 2
SETTINGS_DATE = 3
#KEY = ContainerID VALE =  Present Weight, Previous Weight, Total Refill, Total Consumed, Flag, Start Date 
g_containerStatus = dict()
STATUS_PRESENT_WEIGHT = 0
STATUS_PREVIOUS_WEIGHT = 1
STATUS_TOTAL_REFILL = 2
STATUS_TOTAL_CONSUMED = 3
STATUS_FLAG = 4
STATUS_DATE = 5 
#KEY = Label VALUE =  Container ID, Present Weight, Critical Level, Expiry in Days, Status(Refill/Consumed)
g_containerMessage = dict()
#KEY = Container ID VALUE = Present DATE, Consumend Value
g_perdayConsumption = dict()
CONSUM_DATE = 0
CONSUM_QTY = 1
#KEY = Container ID VALUE = Present DATE, Refill Value
g_perdayRefill = dict()
REFILL_DATE = 0
REFILL_QTY = 1

'''****************************************************************************************

Function Name 	:	ConfigSectionMap
Description		:	Parsing the Config File and Extracting the data and returning it
Parameters 		:	section - section to be parserd

****************************************************************************************'''
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            logging.debug("exception on %s!" % option)
            dict1[option] = None
    return dict1

# Initialize the Pubnub Keys 
PUB_KEY = ConfigSectionMap("pubnub_init")['pub_key']
SUB_KEY = ConfigSectionMap("pubnub_init")['sub_key']

#Database Related Variables and Lists 
DATABASE_TABLE_NAME = ConfigSectionMap("database")['table_name']
DB_USER_NAME = ConfigSectionMap("database")['username']
DB_PASSWORD = ConfigSectionMap("database")['pwd']
COLUMNS = ['SCALE_ID','DATES','TIME','QUANTITY','STATUS']
index = [0]
g_idadb = 0
g_idadf = 0	

DB_URL = 'jdbc:db2://dashdb-entry-yp-dal09-07.services.dal.bluemix.net:50000/BLUDB:user=' + DB_USER_NAME + ';password=' + DB_PASSWORD

'''****************************************************************************************

Function Name 	:	init
Description		:	Initalize the pubnub keys and Starts Subscribing from the 
					kitchenDevice-resp and kitchenApp-req channels
Parameters 		:	None

****************************************************************************************'''
def init():
	#Pubnub Initialization
	global pubnub 
	pubnub = Pubnub(publish_key=PUB_KEY,subscribe_key=SUB_KEY)
	pubnub.subscribe(channels='kitchenDevice-resp', callback=callback, error=callback, reconnect=reconnect, disconnect=disconnect)
	pubnub.subscribe(channels='kitchenApp-req', callback=appcallback, error=appcallback, reconnect=reconnect, disconnect=disconnect)
	
'''****************************************************************************************

Function Name 	:	dB_init
Description		:	Initalize the Database and establishing the connection between the 
					database and the script using the jdbc driver
Parameters 		:	None

****************************************************************************************'''
def dB_init():
	global DATABASE_TABLE_NAME,g_idadb,g_idadf
	l_dbtry = 0
	while(l_dbtry<3):	
		try:
			l_dbtry = 3
			jdbc = DB_URL
			g_idadb = IdaDataBase(jdbc)
			g_idadf = IdaDataFrame(g_idadb,DATABASE_TABLE_NAME)
			logging.info("dashDB-connected")
		except Exception as error:
			l_dbtry += 1
			logging.warning(error)

'''****************************************************************************************

Function Name 	:	defaultLoader
Description		:	Initialize the container Status, loads the container and updates 
					the historical graph
Parameters 		:	None

****************************************************************************************'''
def defaultLoader(p_containerid):
	#KEY = ContainerID VALE =  Present Weight, Previous Weight, Total Refill, Total Consumed, Flag, Start Date 
	g_containerStatus.setdefault(p_containerid, [0.00,0.00,0.00,0.00,False,0])
	#Inital Update for the APP for the Empty Container and Setting UP 
	containerWeight(p_containerid,0.00)
	#Initial Query for the History and Graph
	appHistoricalGraph(p_containerid,TIMESPAN_FOR_HISTORY)
	#Loading the Default Values 
	g_perdayRefill.setdefault(p_containerid, [datetime.datetime.now().date(),0.00])
	g_perdayConsumption.setdefault(p_containerid, [datetime.datetime.now().date(),0])
	#Container Message

'''****************************************************************************************

Function Name 	:	appSetting
Description		:	Handles the Request sent from an app and register the container settings
Parameters 		:	p_requester - Request sent from APP
					p_containerid - Respective Container ID
					p_contatinerlabel - Register the container label for the ID
					p_expiryInMonths - Register the expiry
					p_criticallevel - Register the critical level of the container

****************************************************************************************'''
def appSetting(p_requester,p_containerid,p_containerlabel,p_expiryInMonths,p_criticallevel):
	if(p_requester == "APP"):
		# Container Label, Expiry in Months, Critical Level, End Date
		if(not g_containerSettings.has_key(p_containerid)):
			g_containerSettings[p_containerid] = [p_containerlabel,p_expiryInMonths,p_criticallevel,0]
			defaultLoader(p_containerid)
		else:
			pass
	else:
		pass

'''****************************************************************************************

Function Name 	:	appReset
Description		:	Handles the Request sent from an app and reset the container settings
Parameters 		:	p_requester - Request sent from APP
					p_containerid - Respective Container ID

****************************************************************************************'''
def appReset(p_requester,p_containerid):
	if(p_requester == "APP"):
		if(g_containerSettings.has_key(p_containerid)):
			del g_containerMessage[g_containerSettings[p_containerid][SETTINGS_LABEL]],g_containerSettings[p_containerid]
		else:
			pass
	else:
		pass

'''****************************************************************************************

Function Name 	:	dataBaseUpload
Description		:	Upload the Refill/Consumed Status and Quantity to the DB
Parameters 		:	p_todayDate - Respective Date
					p_containerid - Respective Container ID
					p_status - Status of the Update : Refill/ consumed 
						0 - Refill
						1 - Consumed
					p_quantity - Present Quantity  to be uploaded to DB

****************************************************************************************'''
def dataBaseUpload(p_todayDate,p_containerid,p_status,p_quantity):
	l_checkData_length = 0
	l_time = datetime.datetime.now().strftime('%H:%M:%S')
	l_todays_date = pandas.Timestamp(p_todayDate)
	date_query = "SELECT COUNT(*) FROM DASH5803.HOME1 WHERE DATES = '"+str(p_todayDate)+"'AND STATUS = '"+str(p_status)+"' AND SCALE_ID = '"+p_containerid+"'"
	try:
		l_checkData_length = g_idadb.ida_query(date_query)
	except Exception as error:
		pass
	if(int(l_checkData_length) == 0):
		data = {'SCALE_ID':p_containerid,'DATES':l_todays_date,'TIME':l_time,'QUANTITY':p_quantity,'STATUS':p_status}
		df2 = pandas.DataFrame(data,index = index,columns=COLUMNS)
		g_idadf = IdaDataFrame(g_idadb,DATABASE_TABLE_NAME)
		g_idadb.append(g_idadf,df2,maxnrow = 1)
	else:
		update_query = "UPDATE DASH5803.HOME1 SET TIME = '"+str(l_time)+"', QUANTITY = '"+str(p_quantity)+"' WHERE DATES='" + str(p_todayDate) +"' AND STATUS ='"+str(p_status)+"' AND SCALE_ID = '"+p_containerid+"'"
		l_update = 	g_idadb.ida_query(update_query)

'''****************************************************************************************

Function Name 	:	containerWeight
Description		:	Once the device responses the present weight the server handles the 
					data and evaluvates the container is refilled / consumed
Parameters 		:	p_containerid - Container ID which is updated
					p_weight - Present Weight of the respective container

****************************************************************************************'''
def containerWeight(p_containerid,p_weight):
	global DATABASE_TABLE_NAME,g_idadb,g_idadf
	g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT] =  p_weight
	if(g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT] != g_containerStatus[p_containerid][STATUS_PREVIOUS_WEIGHT]):
		dB_init()
		l_todayDate = datetime.datetime.now().date()
		if(g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT] > g_containerStatus[p_containerid][STATUS_PREVIOUS_WEIGHT]):
			if(g_perdayRefill[p_containerid][REFILL_DATE] != l_todayDate):
				del g_perdayRefill[p_containerid]
				g_perdayRefill.setdefault(p_containerid, [l_todayDate,0.00])
			# Calculate and Update the Per day Refill Value = Per Day Total Refill + current refill
			g_perdayRefill[p_containerid][REFILL_QTY] = g_perdayRefill[p_containerid][REFILL_QTY] + (g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT] -  g_containerStatus[p_containerid][STATUS_PREVIOUS_WEIGHT])
			# Calculate and Update the Total Refill Value  = Total refill + current refill 
			g_containerStatus[p_containerid][STATUS_TOTAL_REFILL] = g_containerStatus[p_containerid][STATUS_TOTAL_REFILL] + (g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT] -  g_containerStatus[p_containerid][STATUS_PREVIOUS_WEIGHT])
			g_containerStatus[p_containerid][STATUS_PREVIOUS_WEIGHT] = g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT]
			g_containerStatus[p_containerid][STATUS_DATE] = datetime.datetime.today()
			g_containerStatus[p_containerid][STATUS_FLAG] = True
			if(g_containerSettings.has_key(p_containerid)):
				# Weight, Critical Level, Expiry in Days, Refill/Consumed
				g_containerSettings[p_containerid][SETTINGS_DATE] = g_containerStatus[p_containerid][STATUS_DATE] + relativedelta(months=+g_containerSettings[p_containerid][SETTINGS_EXPIRY])
				l_expiryInDays =  g_containerSettings[p_containerid][SETTINGS_DATE] - g_containerStatus[p_containerid][STATUS_DATE]
				g_containerMessage[g_containerSettings[p_containerid][SETTINGS_LABEL]] = [p_containerid,p_weight,g_containerSettings[p_containerid][SETTINGS_CRITICAL_LEVEL],l_expiryInDays.days,0]
				pubnub.publish(channel="kitchenApp-resp", message=g_containerMessage)
				#Upload the data to the DB
				dataBaseUpload(l_todayDate,p_containerid,1,g_perdayRefill[p_containerid][REFILL_QTY])
				logging.info("Data Uploaded on Refill") 
		elif(g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT] < g_containerStatus[p_containerid][STATUS_PREVIOUS_WEIGHT]):
			if(g_perdayConsumption[p_containerid][CONSUM_DATE] != l_todayDate):
				del g_perdayConsumption[p_containerid]
				g_perdayConsumption.setdefault(p_containerid, [l_todayDate,0])
			# Calculate and Update the Per day Consumption Value = Consumption + current Consumption
			g_perdayConsumption[p_containerid][CONSUM_QTY] = g_perdayConsumption[p_containerid][CONSUM_QTY] + (g_containerStatus[p_containerid][STATUS_PREVIOUS_WEIGHT] -  g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT])
			# Calculate and Update the Total Consumption Value = Consumption + current Consumption
			g_containerStatus[p_containerid][STATUS_TOTAL_CONSUMED] = g_containerStatus[p_containerid][STATUS_TOTAL_CONSUMED] + (g_containerStatus[p_containerid][STATUS_PREVIOUS_WEIGHT] -  g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT])
			g_containerStatus[p_containerid][STATUS_PREVIOUS_WEIGHT] = g_containerStatus[p_containerid][STATUS_PRESENT_WEIGHT]
			# Avoids Updating the Refill Date for Expiry Calculation
			if(g_containerStatus[p_containerid][STATUS_FLAG]==False):
				g_containerStatus[p_containerid][STATUS_DATE] = datetime.datetime.today()
				g_containerStatus[p_containerid][STATUS_FLAG] = True
			if(g_containerSettings.has_key(p_containerid)):
				if(g_containerSettings[p_containerid][SETTINGS_DATE] == 0):
					g_containerSettings[p_containerid][SETTINGS_DATE] = g_containerStatus[p_containerid][STATUS_DATE] + relativedelta(months=+g_containerSettings[p_containerid][SETTINGS_EXPIRY])
				# Weight, Critical Level, Expiry in Days, Refill/Consumed
				l_expiryInDays =  g_containerSettings[p_containerid][SETTINGS_DATE] - g_containerStatus[p_containerid][STATUS_DATE]
				g_containerMessage[g_containerSettings[p_containerid][SETTINGS_LABEL]] = [p_containerid,p_weight,g_containerSettings[p_containerid][SETTINGS_CRITICAL_LEVEL],l_expiryInDays.days,1]
				pubnub.publish(channel="kitchenApp-resp", message=g_containerMessage)
				#Upload the data to the DB
				dataBaseUpload(l_todayDate,p_containerid,1,g_perdayConsumption[p_containerid][CONSUM_QTY])
				logging.info("Data Uploaded on Consumption")
		else:
			pass			
	else:
		pubnub.publish(channel="kitchenApp-resp", message={g_containerSettings[p_containerid][SETTINGS_LABEL]:[p_containerid,p_weight,g_containerSettings[p_containerid][SETTINGS_CRITICAL_LEVEL],50,0]})
		g_containerMessage[g_containerSettings[p_containerid][SETTINGS_LABEL]] = [p_containerid,p_weight,g_containerSettings[p_containerid][SETTINGS_CRITICAL_LEVEL],50,0]

'''****************************************************************************************

Function Name 	:	appHistoricalGraph
Description		:	Requests the db for the past history with timespan and updates the 
					data to the app
Parameters 		:	p_containerid - Respective contianer
					p_timeSpan - Time Span to request the dB for the data 

****************************************************************************************'''
def appHistoricalGraph(p_containerid,p_timeSpan):
	global DATABASE_TABLE_NAME,g_idadf, g_idadb
	dB_init()
	p_timeSpan = p_timeSpan - 1
	l_refill_history = dict()
	l_consumption_history = dict()
	l_sdat = datetime.datetime.now().date()
	l_edat = l_sdat - datetime.timedelta(days=p_timeSpan)
	l_sdate = l_sdat.strftime('%Y-%m-%d')
	l_edate = l_edat.strftime('%Y-%m-%d')
	# print l_sdate, l_edate
	twodate_query = "SELECT * FROM DASH5803."+ DATABASE_TABLE_NAME +"  WHERE DATES BETWEEN DATE(\'" + l_edate + "\') AND DATE(\'" + l_sdate + "\')"
	l_databaseTableData = []
	l_databaseTableData.append(g_idadb.ida_query(twodate_query))
	l_databaseTableData = l_databaseTableData[0]
	try:
		l_dataOrder = 0
		
		#To Print the database data with timeSpan
		# print l_databaseTableData
		
		#Parsing the data from the database and update the dictionary with respective time span
		for i in range(p_timeSpan,-1,-1):
			l_edat = l_sdat - datetime.timedelta(days=i)
			l_edate = l_edat.strftime('%Y-%m-%d')
			l_refill_history[l_edate] = [p_containerid,0,0,0]
			l_consumption_history[l_edate] = [p_containerid,0,0,0]
		for i,j,k,l,m in zip(l_databaseTableData['SCALE_ID'],l_databaseTableData['DATES'],l_databaseTableData['TIME'],l_databaseTableData['QUANTITY'],l_databaseTableData['STATUS']):
			if(i == p_containerid):
				if m == 0:
					l_refill_history[j] = [i,k,"%.2f"%l,m]
				else:
					l_consumption_history[j] = [i,k,"%.2f"%l,m]
				# Data Publishing with l_refill_history / l_consumption_history: Dates : [container ID,TIME,weight,status(refill/consumed)]
			else:
				pass
	except Exception as occuredError:
		logging.warning(occuredError)
	channel_refill = "kitchenApp-refillHistory-" + p_containerid
	channel_consumption = "kitchenApp-consumptionHistory-" + p_containerid
	pubnub.publish(channel=channel_refill, message=l_refill_history)
	pubnub.publish(channel=channel_consumption, message=l_consumption_history)
	
	#deleting the history 
	del l_databaseTableData,l_refill_history,l_consumption_history

'''****************************************************************************************

Function Name 	:	appUpdate
Description		:	Once the app is loaded, app request for the update. On request the 
					server responds with the current status.
Parameters 		:	p_requester - Request sent from APP

****************************************************************************************'''
def appUpdate(p_requester):
	if p_requester == "APP":
		#Initial Data to be updated with the app
		if(len(g_containerSettings) > 0):
			print g_containerMessage
			pubnub.publish(channel="kitchenApp-resp", message=g_containerMessage)
		else:
			pass
	else:
		pass

'''****************************************************************************************

Function Name 	:	callback
Description		:	Waits for the message from the kitchenDevice-resp channel
Parameters 		:	message - Sensor Status sent from the hardware
					channel - channel for the callback
	
****************************************************************************************'''
def callback(message, channel):
	if(message.has_key("containerID") and message.has_key("weight")):
		containerWeight(message["containerID"],message["weight"])
	else:
		pass

'''****************************************************************************************

Function Name 	:	appcallback
Description		:	Waits for the Request sent from the APP 
Parameters 		:	message - Request sent from the app
					channel - channel for the appcallback

****************************************************************************************'''
def appcallback(message, channel):
	if(message.has_key("requester") and message.has_key("requestType")):
		if(message["requestType"] == 0):
			appSetting(message["requester"],message["containerID"],message["containerLabel"],message["expiryMonths"],message["criticalLevel"])
		elif(message["requestType"] == 1):
			appReset(message["requester"],message["containerID"])
		elif(message["requestType"] == 2):
			appHistoricalGraph(message["containerID"],message["timeSpan"])
		elif(message["requestType"] == 3):
			appUpdate(message["requester"])
	else:
		pass

'''****************************************************************************************

Function Name 	:	error
Description		:	If error in the channel, prints the error
Parameters 		:	message - error message

****************************************************************************************'''
def error(message):
	pass
    # logging.debug("ERROR : " + str(message))

'''****************************************************************************************

Function Name 	:	reconnect
Description		:	Responds if server connects with pubnub
Parameters 		:	message

****************************************************************************************'''
def reconnect(message):
    logging.info("RECONNECTED")

'''****************************************************************************************

Function Name 	:	disconnect
Description		:	Responds if server disconnects from pubnub
Parameters 		:	message

****************************************************************************************'''
def disconnect(message):
    logging.info("DISCONNECTED")
	
if __name__ == '__main__':
	#Initialize the Script
	init()

#End of the Script 
##*****************************************************************************************************##

