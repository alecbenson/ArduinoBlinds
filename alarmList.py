import datetime
from alarm import Alarm
import threading

class AlarmList:
        def __init__(self, interval):
                self.list = []
                self.now = datetime.datetime.now() 
                self.hour = self.now.hour
                self.minute = self.now.minute
                self.parsed = str(self.hour) + ":" + str(self.minute)
                self.object = Alarm( self.parsed )
                self.interval = interval

        #adds an alarm to the list of alarms
        def add(self, alarm ):
                if( alarm.repeat ):
                        alarm.writeToSaved()

                for addedAlarms in self.list:
                        if addedAlarms.time == alarm.time:
                                return 

                self.list.append( alarm )
                #self.list.sort( self.compare )
                self.list.sort( key=lambda x: x.time)
                self.check()
                print("Added alarm with time " + alarm.time )

        #removes an alarm from the list of alarms
        def remove(self, index ):
                self.list.pop(index)

        #import saved alarms from savedAlarms.xml into the list of alarms
        def importSavedAlarms(self):
                for alarm in root:
                        time = alarm.get('time')
                        action = alarm.get('action')
                        savedAlarm = alarm(time, action, True)
                        self.add(savedAlarm)

        #check for queued alarms
        def check(self):
                if len( self.list ) != 0:
                        print("Checked alarm list at " + self.object.time )
                        nextAlarm = self.list[0]

                        if nextAlarm.time <= self.object.time :
                                nextAlarm.trigger()
                                self.remove(0)

                        midnight = "00:01"
                        if self.object.time == midnight:
                                self.importSavedAlarms()

                threading.Timer( self.interval, self.check ).start()

        def prettyAlarmList(self):
                prettyList = []
                for alarms in self.list:
                        action = " - Open" if alarms.action else " - Close"
                        repeating = " - Repeating" if alarms.repeat else " - Non-repeating"
                        formattedAlarm = alarms.time + action + repeating
                        prettyList.append(formattedAlarm)
                return prettyList
