import time
from alarm import Alarm
import threading
import xml.etree.ElementTree as ET
import datetime

class AlarmList:
        def __init__(self, interval):
                self.interval = interval


        #removes an alarm from the list of saved alarms
        def remove(self, index):
                tree = ET.parse('savedAlarms.xml')
                root = tree.getroot()
                time = self.getLocalTime()
                count = 0;
                for alarm in root:
                        if(index != count):
                                count += 1
                                continue
                        else:
                                root.remove(alarm)
                                break
                tree.write('savedAlarms.xml')

        #retrieves the current time
        def getLocalTime(self):
                timeElements = []
                localTime = time.localtime()
                hour = str(localTime[3]).zfill(2)
                minute = str(localTime[4]).zfill(2)
                parsed = hour + ":" + minute
                timeElements.append(hour)
                timeElements.append(minute)
                timeElements.append(parsed)
                return timeElements

        #retrieves the current date
        def getDate(self):
                dateElements = []
                date = datetime.datetime.now()
                dateElements.append(date.year)
                dateElements.append(date.month)
                dateElements.append(date.day)
                return dateElements

        #checks for triggerable alarms
        def check(self):
                tree = ET.parse('savedAlarms.xml')
                root = tree.getroot()
                localTime = self.getLocalTime()
                index = 0
                print("Checking alarms")
                if len(root) != 0:
                        for alarm in root:
                                time = alarm.get('time')
                                action = alarm.get('action')
                                occurrence = alarm.get('occurrence')
                                savedAlarm = Alarm(time, action, occurrence)

                                if localTime[2] == savedAlarm.time:
                                        if self.getDate() == savedAlarm.getDate():
                                                savedAlarm.trigger()
                                                self.remove(index)
                                        elif savedAlarm.getDate() == "repeating":
                                                savedAlarm.trigger()
                                else:
                                        index += 1
                                        continue
                threading.Timer( self.interval, self.check ).start()
                                

        def prettyAlarmList(self):
                tree = ET.parse('savedAlarms.xml')
                root = tree.getroot()
                time = self.getLocalTime()
                prettyList = []
                for alarm in root:
                        time = alarm.get('time')
                        action = int(alarm.get('action'))
                        occurrence = alarm.get('occurrence')

                        action = "open" if action else "close"
                        occurrence = alarm.get('occurrence')
                        formattedAlarm = "The blinds will " + action + " at " + time + " (" + occurrence + ")"
                        prettyList.append(formattedAlarm)
                return prettyList
