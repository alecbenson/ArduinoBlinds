import time
import datetime
import threading
from serial import Serial
import glob
import xml.etree.ElementTree as ET

alarmList = []
tree = ET.parse('savedAlarms.xml')
root = tree.getroot()

#Checks to see if an alarm needs to be triggered
def checkTime():
	if len(alarmList) != 0:
		currentTime = datetime.datetime.now()
		currentHour = currentTime.hour
		currentMinute = currentTime.minute
		parsedTime = parseTime( currentHour, currentMinute )
		print("Checked alarm list at " + parsedTime)

		nextAlarm = alarmList[0]
		nextAlarmSplit = splitParsedTime(nextAlarm)

		#If it is time to trigger the next alarm..
		if compareTime(parsedTime, nextAlarm) >= 0:
			print("Triggering alarm: " + nextAlarm)
			triggerAlarm()
			removeAlarm(0)
		#Add saved alarms back after midnight
		if compareTime(parsedTime, "00:01") == 0:
			addSavedAlarms()

	#check the time again in 60 seconds
	threading.Timer(60, checkTime).start()

#adds an alarm to the list of alarms
def addAlarm( time, continuous):
	if(continuous):
		saveAlarm(time)

	if time in alarmList:
		return

	alarmTime = time
	alarmList.append(alarmTime)
	alarmList.sort(compareTime)
	print("Added alarm with time " + alarmTime)

#Save an alarm to savedAlarms.xml
def saveAlarm( time ):
	for alarm in root:
		if alarm.get('time') == time:
			return

	newAlarm = ET.Element("alarm")
	newAlarm.set("time",time)
	root.append(newAlarm)
	tree.write("savedAlarms.xml")
	print("Saved repeating alarm")

#import saved alarms from savedAlarms.xml into the list of alarms
def addSavedAlarms():
	for alarm in root:
		addTime = alarm.get('time')
		addAlarm( addTime, False)

#removes an alarm from the list of alarms
def removeAlarm(index):
	alarmList.pop(index)

#parses the time in a nice, managable format
def parseTime(hour, minute):
	return str(hour) + ":" + str(minute)

#splits the parsed time back into hours and minutes
def splitParsedTime(timeString):
	return timeString.split(":")

#used to compare one time against another for sorting
def compareTime(time1, time2):
	time1 = splitParsedTime(time1)
	time2 = splitParsedTime(time2)

	if int(time1[0]) > int(time2[0]):
		return 1
	elif int(time1[0]) < int(time2[0]):
		return -1
	else:
		if int(time1[1]) > int(time2[1]):
			return 1
		elif int(time1[1]) < int(time2[1]): 
			return -1
		else:
			return 0

#Sends a signal to the arduino that it needs to move
def triggerAlarm():
	port = glob.glob("/dev/ttyACM*")
	port = port[0]
	ser = Serial( port, 9600, timeout=1)
	print("Sent trigger signal to: " + ser.portstr)

	time.sleep(1)
	ser.write('b')
	ser.close()