'''*********************************************************************************
SERVER - KITCHEN TRACKER
*********************************************************************************'''
#Import the Modules Required
from pubnub import Pubnub
import datetime
from dateutil.relativedelta import relativedelta

# Modules for the dashDB
import ibmdbpy
from ibmdbpy.base import IdaDataBase
from ibmdbpy.frame import IdaDataFrame
from pandas import DataFrame
import pandas

dbname = 'HOME1'
columns = ['SCALE_ID','DATES','TIME','QUANTITY','STATUS']
index = [0]
idadb = 0
idadf = 0	

# Initialize the Pubnub Keys 
pub_key = "pub-c-913ab39c-d613-44b3-8622-2e56b8f5ea6d"
sub_key = "sub-c-8ad89b4e-a95e-11e5-a65d-02ee2ddab7fe"

g_containerSettings = dict()
g_containerStatus = dict()
g_containerMessage = dict()
g_perdayConsumption = dict()
g_perdayRefill = dict()
l_json_dict = dict()
l_json_dict1 = dict()
'''****************************************************************************************

Function Name 	:	init
Description		:	Initalize the pubnub keys and Starts Subscribing from the 
					kitchenDevice-resp and kitchenApp-req channels
Parameters 		:	None

****************************************************************************************'''
def init():
	#Pubnub Initialization
	global pubnub 
	pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key)
	pubnub.subscribe(channels='kitchenDevice-resp', callback=callback, error=callback, reconnect=reconnect, disconnect=disconnect)
	pubnub.subscribe(channels='kitchenApp-req', callback=appcallback, error=appcallback, reconnect=reconnect, disconnect=disconnect)

'''****************************************************************************************

Function Name 	:	containerWeight
Description		:	Handles the Request sent from an app and makes the settings
Parameters 		:	p_requester - Request sent from APP

****************************************************************************************'''
def containerWeight(p_containerid,p_weight):
	global dbname,idadb,idadf
	try:
		jdbc = 'jdbc:db2://dashdb-entry-yp-dal09-07.services.dal.bluemix.net:50000/BLUDB:user=dash5803;password=1jBKYZa9q3yG' 
		idadb = IdaDataBase(jdbc)
		idadf = IdaDataFrame(idadb,dbname)
		print 'dashDB-connected'
	except Exception as e:
		print e


	#Present Weight, Previous Weight, Total Refill, Total Consumed, Flag, Start Date
	if(not g_containerStatus.has_key(p_containerid)): 
		g_containerStatus[p_containerid] = [0.00,0.00,0.00,0.00,False,0]
	else:
		g_containerStatus[p_containerid][0] =  p_weight
		if(g_containerStatus[p_containerid][0] != g_containerStatus[p_containerid][1]):
			if(g_containerStatus[p_containerid][0] > g_containerStatus[p_containerid][1]):
				l_todayDate = datetime.datetime.now().date()
				l_todays_date = pandas.Timestamp(l_todayDate)
				l_endTime = datetime.datetime.now()
				l_time = str(l_endTime.hour) + ":" + str(l_endTime.minute) + ":" + str(l_endTime.second)
				if(not g_perdayRefill.has_key(l_todayDate)):
					g_perdayRefill[l_todayDate] = 0					
				g_perdayRefill[l_todayDate] = g_perdayRefill[l_todayDate] + (g_containerStatus[p_containerid][0] -  g_containerStatus[p_containerid][1])
				g_containerStatus[p_containerid][2] = g_containerStatus[p_containerid][2] + (g_containerStatus[p_containerid][0] -  g_containerStatus[p_containerid][1])
				g_containerStatus[p_containerid][1] = g_containerStatus[p_containerid][0]
				g_containerStatus[p_containerid][5] = datetime.datetime.today()
				g_containerStatus[p_containerid][4] = True
				if(g_containerSettings.has_key(p_containerid)):
					# Weight, Critical Level, Expiry in Days, Refill/Consumed
					g_containerSettings[p_containerid][3] = g_containerStatus[p_containerid][5] + relativedelta(months=+g_containerSettings[p_containerid][1])
					l_expiryInDays =  g_containerSettings[p_containerid][3] - g_containerStatus[p_containerid][5]
					g_containerMessage[g_containerSettings[p_containerid][0]] = [p_containerid,p_weight,g_containerSettings[p_containerid][2],l_expiryInDays.days,0]
					l_checkData_length = 0
					date_query = "SELECT COUNT(*) FROM DASH5803.HOME1 WHERE DATES = '"+str(l_todayDate)+"' AND STATUS = '0'"
					print date_query
					l_checkData_length = idadb.ida_query(date_query)
					print l_checkData_length
					if(int(l_checkData_length) == 0):
						data = {'SCALE_ID':p_containerid,'DATES':l_todays_date,'TIME':l_time,'QUANTITY':g_perdayRefill[l_todayDate],'STATUS':0}
						df2 = pandas.DataFrame(data,index = index,columns=columns)
						idadf = IdaDataFrame(idadb,dbname)
						idadb.append(idadf,df2,maxnrow = 1)
					else:
						update_query = "UPDATE DASH5803.HOME1 SET TIME = '"+str(l_time)+"', QUANTITY = '"+str(g_perdayRefill[l_todayDate])+"' WHERE DATES='" + str(l_todayDate) +"' AND STATUS ='0'"
						l_update = 	idadb.ida_query(update_query)					
					print "Data Uploaded on Refill"
					pubnub.publish(channel="kitchenApp-resp", message=g_containerMessage)

			elif(g_containerStatus[p_containerid][0] < g_containerStatus[p_containerid][1]):
				l_todayDate = datetime.datetime.now().date()
				l_todays_date = pandas.Timestamp(l_todayDate)
				l_endTime = datetime.datetime.now()
				l_time = str(l_endTime.hour) + ":" + str(l_endTime.minute) + ":" + str(l_endTime.second)
				if(not g_perdayConsumption.has_key(l_todayDate)):
					g_perdayConsumption[l_todayDate] = 0					
				l_itemConsumption = (g_containerStatus[p_containerid][1] -  g_containerStatus[p_containerid][0])
				g_containerStatus[p_containerid][3] = g_containerStatus[p_containerid][3] + l_itemConsumption
				g_containerStatus[p_containerid][1] = g_containerStatus[p_containerid][0]
				g_perdayConsumption[l_todayDate] = g_perdayConsumption[l_todayDate] + l_itemConsumption
				if(g_containerStatus[p_containerid][4]==False):
					g_containerStatus[p_containerid][5] = datetime.datetime.today()
					g_containerStatus[p_containerid][4] = True
				if(g_containerSettings.has_key(p_containerid)):
					if(g_containerSettings[p_containerid][3] == 0):
						g_containerSettings[p_containerid][3] = g_containerStatus[p_containerid][5] + relativedelta(months=+g_containerSettings[p_containerid][1])
					# Weight, Critical Level, Expiry in Days, Refill/Consumed
					l_expiryInDays =  g_containerSettings[p_containerid][3] - g_containerStatus[p_containerid][5]
					g_containerMessage[g_containerSettings[p_containerid][0]] = [p_containerid,p_weight,g_containerSettings[p_containerid][2],l_expiryInDays.days,1]
					l_checkData_length = 0
					date_query = "SELECT COUNT(*) FROM DASH5803.HOME1 WHERE DATES = '"+str(l_todayDate)+"'AND STATUS = '1'"
					l_checkData_length = idadb.ida_query(date_query)
					if(int(l_checkData_length) == 0):
						data = {'SCALE_ID':p_containerid,'DATES':l_todays_date,'TIME':l_time,'QUANTITY':g_perdayConsumption[l_todayDate],'STATUS':1}
						df2 = pandas.DataFrame(data,index = index,columns=columns)
						idadf = IdaDataFrame(idadb,dbname)
						idadb.append(idadf,df2,maxnrow = 1)
					else:
						update_query = "UPDATE DASH5803.HOME1 SET TIME = '"+str(l_time)+"', QUANTITY = '"+str(g_perdayConsumption[l_todayDate])+"' WHERE DATES='" + str(l_todayDate) +"' AND STATUS ='1'"
						l_update = 	idadb.ida_query(update_query)
					print "Data Uploaded on Consumption"
					pubnub.publish(channel="kitchenApp-resp", message=g_containerMessage)
			print g_containerStatus
			# idadb.close()
		else:
			pass


'''****************************************************************************************

Function Name 	:	appSetting
Description		:	Handles the Request sent from an app and makes the settings
Parameters 		:	p_requester - Request sent from APP

****************************************************************************************'''
def appSetting(p_requester,p_containerid,p_containerlabel,p_expiryInMonths,p_criticallevel):
	if(p_requester == "APP"):
		# Container Label, Expiry in Months, Critical Level, End Date
		if(not g_containerSettings.has_key(p_containerid)):
			g_containerSettings[p_containerid] = [p_containerlabel,p_expiryInMonths,p_criticallevel,0]
		else:
			g_containerSettings[p_containerid] = [p_containerlabel,p_expiryInMonths,p_criticallevel,0]
	else:
		pass

'''****************************************************************************************

Function Name 	:	appReset
Description		:	Handles the Request sent from an app and makes the settings
Parameters 		:	p_requester - Request sent from APP

****************************************************************************************'''
def appReset(p_requester,p_containerid):
	if(p_requester == "APP"):
		if(g_containerSettings.has_key(p_containerid)):
			del g_containerSettings[p_containerid]
		else:
			pass
	else:
		pass

'''****************************************************************************************

Function Name 	:	appHistoricalGraph
Description		:	Handles the Request sent from an app and makes the settings
Parameters 		:	p_requester - Request sent from APP

****************************************************************************************'''
def appHistoricalGraph(p_requester,p_containerid,p_timeSpan):
	global dbname,idadf, idadb
	try:
		jdbc = 'jdbc:db2://dashdb-entry-yp-dal09-07.services.dal.bluemix.net:50000/BLUDB:user=dash5803;password=1jBKYZa9q3yG' 
		idadb = IdaDataBase(jdbc)
		print 'DB Connected for HSG'
	except Exception as e:
		print e
	idadf = IdaDataFrame(idadb,dbname)
	l_sdat = datetime.datetime.now().date()
	if(p_requester == "APP"):
		if(p_timeSpan == 7):
			l_edat = l_sdat - datetime.timedelta(days=p_timeSpan)
			l = l_edat.strftime('%Y-%m-%d')
			l_sdate = l_sdat.strftime('%Y-%m-%d')
			l_edate = l_edat.strftime('%Y-%m-%d')
			twodate_query = "SELECT * FROM DASH5803."+ dbname +" WHERE DATES BETWEEN DATE(\'" + l_edate + "\') AND DATE(\'" + l_sdate + "\')"
			l_databaseTableData = []
			l_databaseTableData.append(idadb.ida_query(twodate_query))
			l_databaseTableData = l_databaseTableData[0]
			try:
				l_dataOrder = 0
				for i in range(6,-1,-1):
					l_edat = l_sdat - datetime.timedelta(days=i)
					l_edate = l_edat.strftime('%Y-%m-%d')
					l_json_dict[l_edate] = [p_containerid,0,0,0]
					l_json_dict1[l_edate] = [p_containerid,0,0,0]
				for i,j,k,l,m in zip(l_databaseTableData['SCALE_ID'],l_databaseTableData['DATES'],l_databaseTableData['TIME'],l_databaseTableData['QUANTITY'],l_databaseTableData['STATUS']):
					if(i == p_containerid):
						if m == 0:
							l_json_dict[j] = [i,k,"%.2f"%l,m]
						else:
							l_json_dict1[j] = [i,k,"%.2f"%l,m]
					else:
						pass
			except Exception as e:
				print e
		else:
			l_edat = l_sdat - datetime.timedelta(days=p_timeSpan)
			l_sdate = str(l_sdat.year) + "-" + str(l_sdat.month) + "-" + str(l_sdat.day)
			l_edate = str(l_edat.year) + "-" + str(l_edat.month) + "-" + str(l_edat.day)
			twodate_query = "SELECT * FROM DASH5803."+ dbname +"  WHERE DATES BETWEEN DATE(\'" + l_edate + "\') AND DATE(\'" + l_sdate + "\')"
			l_databaseTableData = []
			l_databaseTableData.append(idadb.ida_query(twodate_query))
			l_databaseTableData = l_databaseTableData[0]
			try:
				l_dataOrder = 0
				print l_databaseTableData
				for i in range(6,-1,-1):
					l_edat = l_sdat - datetime.timedelta(days=i)
					l_edate = l_edat.strftime('%Y-%m-%d')
					l_json_dict[l_edate] = [p_containerid,0,0,0]
					l_json_dict1[l_edate] = [p_containerid,0,0,0]
				for i,j,k,l,m in zip(l_databaseTableData['SCALE_ID'],l_databaseTableData['DATES'],l_databaseTableData['TIME'],l_databaseTableData['QUANTITY'],l_databaseTableData['STATUS']):
					if(i == p_containerid):
						if m == 0:
							l_json_dict[j] = [i,k,"%.2f"%l,m]
						else:
							l_json_dict1[j] = [i,k,"%.2f"%l,m]
					else:
						pass
			except Exception as e:
				print e
		print l_json_dict,l_json_dict1
		print pubnub.publish(channel="kitchenApp-resp1", message=l_json_dict)
		print pubnub.publish(channel="kitchenApp-resp2", message=l_json_dict1)
		del l_databaseTableData
	else:
		pass

'''****************************************************************************************

Function Name 	:	appUpdate
Description		:	Handles the Request sent from an app and makes the settings
Parameters 		:	p_requester - Request sent from APP

****************************************************************************************'''
def appUpdate(p_requester):
	if p_requester == "APP":
		print pubnub.publish(channel="kitchenApp-resp", message=g_containerMessage)
		print pubnub.publish(channel="kitchenApp-resp1", message=l_json_dict)
		print pubnub.publish(channel="kitchenApp-resp2", message=l_json_dict1)
	else:
		pass

'''****************************************************************************************

Function Name 	:	callback
Description		:	Waits for the message from the kitchenDevice-resp channel
Parameters 		:	message - Sensor Status sent from the hardware
					channel - channel for the callback
	
****************************************************************************************'''
def callback(message, channel):
	print message
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
	print message
	if(message.has_key("requester") and message.has_key("requestType")):
		if(message["requestType"] == 0):
			appSetting(message["requester"],message["containerID"],message["containerLabel"],message["expiryMonths"],message["criticalLevel"])
		elif(message["requestType"] == 1):
			appReset(message["requester"],message["containerID"])
		elif(message["requestType"] == 2):
			appHistoricalGraph(message["requester"],message["containerID"],message["timeSpan"])
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
    print("ERROR : " + str(message))

'''****************************************************************************************

Function Name 	:	reconnect
Description		:	Responds if server connects with pubnub
Parameters 		:	message

****************************************************************************************'''
def reconnect(message):
    print("RECONNECTED")

'''****************************************************************************************

Function Name 	:	disconnect
Description		:	Responds if server disconnects from pubnub
Parameters 		:	message

****************************************************************************************'''
def disconnect(message):
    print("DISCONNECTED")
	
if __name__ == '__main__':
	#Initialize the Script
	init()

#End of the Script 
##*****************************************************************************************************##

