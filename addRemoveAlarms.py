import time
import datetime
import threading
from serial import Serial
import glob

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

		#If it is time to trigger the next alarm..
		if compareTime(parsedTime, nextAlarm) >= 0:
			print("Triggering alarm: " + nextAlarm)
			triggerAlarm()
			removeAlarm(0)

	#check the time again in 60 seconds
	threading.Timer(1, checkTime).start()

#adds an alarm to the list of alarms
def addAlarm(hour, minute):
	alarmTime = parseTime(hour,minute)
	alarmList.append(alarmTime)
	alarmList.sort(compareTime)
	print("Added alarm with time " + alarmTime)

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

#Sends a signal to the arduino that it needs to move
def triggerAlarm():
	port = glob.glob("/dev/ttyACM*")
	port = port[0]
	ser = Serial( port, 9600, timeout=1)

	print("Sent trigger signal to: " + ser.portstr)
	
	#'a' tells the arduino to turn clockwise
	ser.write('a')
	ser.close()

