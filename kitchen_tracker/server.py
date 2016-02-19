'''*********************************************************************************
SERVER - KITCHEN TRACKER
*********************************************************************************'''
#Import the Modules Required
from pubnub import Pubnub
import datetime
from dateutil.relativedelta import relativedelta

# Initialize the Pubnub Keys 
pub_key = "pub-c-913ab39c-d613-44b3-8622-2e56b8f5ea6d"
sub_key = "sub-c-8ad89b4e-a95e-11e5-a65d-02ee2ddab7fe"

g_containerSettings = dict()
g_containerStatus = dict()
g_containerMessage = dict()
g_perdayConsumption = dict()
'''****************************************************************************************

Function Name 	:	init
Description	:	Initalize the pubnub keys and Starts Subscribing from the 
			parkingdevice-resp and parkingapp-req channels
Parameters 	:	None

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
	#Present Weight, Previous Weight, Total Refill, Total Consumed, Flag, Start Date
	if(not g_containerStatus.has_key(p_containerid)): 
		g_containerStatus[p_containerid] = [0.00,0.00,0.00,0.00,False,0]
	else:
		g_containerStatus[p_containerid][0] =  p_weight
		if(g_containerStatus[p_containerid][0] != g_containerStatus[p_containerid][1]):
			if(g_containerStatus[p_containerid][0] > g_containerStatus[p_containerid][1]):
				g_containerStatus[p_containerid][2] = g_containerStatus[p_containerid][2] + (g_containerStatus[p_containerid][0] -  g_containerStatus[p_containerid][1])
				g_containerStatus[p_containerid][1] = g_containerStatus[p_containerid][0]
				g_containerStatus[p_containerid][5] = datetime.datetime.today()
				g_containerStatus[p_containerid][4] = True
				if(g_containerSettings.has_key(p_containerid)):
					# Weight, Critical Level, Expiry in Days, Refill/Consumed
					g_containerSettings[p_containerid][3] = g_containerStatus[p_containerid][5] + relativedelta(months=+g_containerSettings[p_containerid][1])
					l_expiryInDays =  g_containerSettings[p_containerid][3] - g_containerStatus[p_containerid][5]
					g_containerMessage[g_containerSettings[p_containerid][0]] = [p_weight,g_containerSettings[p_containerid][2],l_expiryInDays.days,"Item Refilled"]
					print g_containerMessage
					# pubnub.publish(channel="kitchenApp-resp", message=g_containerMessage[p_containerid])
			elif(g_containerStatus[p_containerid][0] < g_containerStatus[p_containerid][1]):
				l_todayDate = datetime.datetime.today()
				l_todayDate = l_todayDate.date()
				if(not g_perdayConsumption.has_key(l_todayDate)):
					g_perdayConsumption[l_todayDate] = 0					
				l_itemConsumption = (g_containerStatus[p_containerid][1] -  g_containerStatus[p_containerid][0])
				g_containerStatus[p_containerid][3] = g_containerStatus[p_containerid][3] + l_itemConsumption
				g_containerStatus[p_containerid][1] = g_containerStatus[p_containerid][0]
				g_perdayConsumption[l_todayDate] = g_perdayConsumption[l_todayDate] + l_itemConsumption
				l_perdayConsumption = str(l_todayDate.year) + "/" + str(l_todayDate.month) + "/" + str(l_todayDate.day)
				print l_perdayConsumption, g_perdayConsumption
				if(g_containerStatus[p_containerid][4]==False):
					g_containerStatus[p_containerid][5] = datetime.datetime.today()
					g_containerStatus[p_containerid][4] = True
				if(g_containerSettings.has_key(p_containerid)):
					if(g_containerSettings[p_containerid][3] == 0):
						g_containerSettings[p_containerid][3] = g_containerStatus[p_containerid][5] + relativedelta(months=+g_containerSettings[p_containerid][1])
					# Weight, Critical Level, Expiry in Days, Refill/Consumed
					l_expiryInDays =  g_containerSettings[p_containerid][3] - g_containerStatus[p_containerid][5]
					g_containerMessage[g_containerSettings[p_containerid][0]] = [p_weight,g_containerSettings[p_containerid][2],l_expiryInDays.days,"Item Consumed"]
					print g_containerMessage
					# pubnub.publish(channel="kitchenApp-resp", message=g_containerMessage[p_containerid])
			print g_containerStatus
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
			g_containerSettings[p_containerid] = [p_containerlabel,0,p_criticallevel,0]
			g_containerSettings[p_containerid][1] = p_expiryInMonths
		else:
			pass
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
def appHistoricalGraph(p_requester,p_containerid):
	if(p_requester == "APP"):
			print g_perdayConsumption
	else:
		pass

'''****************************************************************************************

Function Name 	:	appUpdate
Description		:	Handles the Request sent from an app and makes the settings
Parameters 		:	p_requester - Request sent from APP

****************************************************************************************'''
def appUpdate(p_requester):
	if(p_requester == "APP"):
		print g_containerMessage
		# pubnub.publish(channel="kitchenApp-resp", message=g_containerMessage)
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
			appHistoricalGraph(message["requester"],message["containerID"])
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

'''****************************************************************************************

Function Name 	:	__main__
Description		:	Conditional Stanza where the Script starts to run
Parameters 		:	None

****************************************************************************************'''
if __name__ == '__main__':
	#Initialize the Script
	init()

#End of the Script 
##*****************************************************************************************************##

