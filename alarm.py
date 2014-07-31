import glob
import time
import xml.etree.ElementTree as ET
from serial import Serial

class Alarm:
	def __init__(self, time="00:01", action=0, occurrence="0000-00-00"):
		self.time = time
		self.action = int(action)
		self.occurrence = occurrence
		self.hour = int(time.split(":")[0])
		self.minute = int(time.split(":")[1])
		self.occurrence = occurrence;

		#If the date is not repeating, it will have 3 components


	#Save an alarm to savedAlarms.xml
	def saveAlarm(self):
		tree = ET.parse('savedAlarms.xml')
		root = tree.getroot()
		for alarm in root:
			if alarm.get('time') == self.time:
				return

		newAlarm = ET.Element("alarm")
		newAlarm.set("time", self.time)
		newAlarm.set("action", str(self.action) )
		newAlarm.set("occurrence", str(self.occurrence) )
		root.append(newAlarm)
		tree.write("savedAlarms.xml")
		print("Saved alarm")

	def getDate(self):
		occurrence = self.occurrence.split("-")
		try:
			return [int(dateElement) for dateElement in occurrence]
		except:
			return "repeating"


	#Sends a signal to the arduino that it needs to move
	def trigger(self):
		port = glob.glob("/dev/ttyACM*")
		port = port[0]
		ser = Serial( port, 9600, timeout=1)
		print("Sent trigger signal to: " + ser.portstr)
		
		time.sleep(1)

		if self.action == 1:
			ser.write('b') #Open the blinds
		else:
			ser.write('a') #Close the blinds

		ser.close()




#changed writetoSaved to saveAlarm