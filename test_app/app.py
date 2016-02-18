'''*********************************************************************************
TESTAPP - KITCHEN TRACKER
*********************************************************************************'''
from pubnub import Pubnub
from threading import Thread
import sys

pub_key = "pub-c-913ab39c-d613-44b3-8622-2e56b8f5ea6d"
sub_key = "sub-c-8ad89b4e-a95e-11e5-a65d-02ee2ddab7fe"

g_kitchenData = dict()

def init():
	#Pubnub Key Initialization
	global pubnub 
	pubnub = Pubnub(publish_key=pub_key,subscribe_key=sub_key)
	pubnub.subscribe(channels='kitchenApp-resp', callback=callback, error=callback,
					connect=connect, reconnect=reconnect, disconnect=disconnect)

def callback(message, channel):
	g_kitchenData.update(message)

def dataHandling(stdin):
		l_action = int(stdin.readline().strip())
		if(l_action == 0):
			pubnub.publish(channel='kitchenApp-req',message={"requester":"APP","requestType":0, "containerID":"002",
							"expiryMonths":3, "containerLabel":"RICE", "criticalLevel":0.5})
		elif(l_action == 1):
			pubnub.publish(channel='kitchenApp-req', 
					message={"requester":"APP","requestType":1, "containerID":"002"})
		elif(l_action == 2):
			pubnub.publish(channel='kitchenApp-req', 
					message={"requester":"APP","requestType":2, "containerID":"002"})
		elif(l_action == 3):
			pubnub.publish(channel='kitchenApp-req', 
					message={"requester":"APP","requestType":3})
		elif(l_action == 4):
			print g_kitchenData
		else:
			pass
			
def error(message):
    print("ERROR : " + str(message))
  
def connect(message):
    print "CONNECTED"
  
def reconnect(message):
	print("RECONNECTED")
  
def disconnect(message):
	print("DISCONNECTED")

if __name__ == '__main__':
	init()
	while True:
		t1 = Thread(target=dataHandling, args=(sys.stdin,))
		t1.start()
		t1.join()

		
#End of the Script 
##*****************************************************************************************************##
	