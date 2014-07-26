import time
import datetime
import glob
import threading
from serial import Serial

alarmList = []

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

		if compareTime(parsedTime, nextAlarm) >= 0:
			print("Triggering alarm: " + nextAlarm)
			triggerAlarm( nextAlarmSplit[0], nextAlarmSplit[1] )
			removeAlarm(0)

	#check the time again in 60 seconds
	threading.Timer(1, checkTime).start()

#Sends a signal to the arduino that it needs to move
def triggerAlarm(hour, minute):
	port = glob.glob("/dev/ttyACM*")
	print("Autodetected port " + port[0])
	port = port[0]
			
	ser = Serial(port, 9600, timeout=1)
	print("Successfully connected to: " + ser.portstr)
	
	#'a' tells the arduino to turn clockwise
	ser.write('a')
	print( parseTime(hour,minute) )
	addAlarm(hour,minute)
	return json.dumps(alarmList)
	ser.close()

#adds an alarm to the list of alarms
def addAlarm(hour, minute):
	alarmTime = parseTime(hour,minute)
	alarmList.append(alarmTime)
	alarmList.sort(compareTime)
	print(alarmList)

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

	if time1[0] > time2[0]:
		return 1
	elif time1[0] < time2[0]:
		return -1
	else:
		if time1[1] > time2[1]:
			return 1
		elif time1[1] < time2[1]: 
			return -1
		else:
			return 0

