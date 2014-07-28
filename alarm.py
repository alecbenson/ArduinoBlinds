import glob
import time
import xml.etree.ElementTree as ET
from serial import Serial

class Alarm:
	def __init__(self, time="00:01", action=0, repeat=False):
		self.time = time
		self.action = int(action)
		self.repeat = int(repeat)
		self.hour = int(time.split(":")[0])
		self.minute = int(time.split(":")[1])

	#Save an alarm to savedAlarms.xml
	def writeToSaved(self):
		tree = ET.parse('savedAlarms.xml')
		root = tree.getroot()
		for alarm in root:
			if alarm.get('time') == self.time:
				return

		newAlarm = ET.Element("alarm")
		newAlarm.set("time", self.time)
		newAlarm.set("action", str(self.action) )
		root.append(newAlarm)
		tree.write("savedAlarms.xml")
		print("Saved repeating alarm")

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




