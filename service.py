#usr/bin/python3
import sys
import web
import json
from alarm import Alarm
from alarmList import AlarmList

urls = (
        '/', 'GetAlarms',
        '/add', 'Add',
        '/action', 'Action',
        '/remove', 'Remove'
        )

alarmList = AlarmList(60)

if __name__ == "__main__":
        alarmList.check()
        app = web.application(urls, globals() )
        app.run()

#Immedietly open or close the blinds
class Action:
        def GET(self):
                global alarmList
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback
                params = web.input()
                actionRequest = int( json.dumps( params.action)[1:-1] )

                openAlarm = Alarm(action=1)
                closeAlarm = Alarm(action=0)
                if actionRequest:
                        openAlarm.trigger()
                else:
                        closeAlarm.trigger()
                return '%s(%s)' % (callbackName, "console.log('Action completed')" )

#Retrieve a list of alarms
class GetAlarms:
        def GET(self):
                global alarmList
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback
                return '%s(%s)' % (callbackName, alarmList.prettyAlarmList() )

#Remove the alarm at the specified index
class Remove:
        def GET(self):
                global alarmList
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback
                params = web.input()
                index = int( json.dumps( params.index )[1:-1] )
                alarmList.remove( index )
                return '%s(%s)' % (callbackName, alarmList.prettyAlarmList() )

#Add an alarm to the saved alarms
class Add:
        def GET(self):
                global alarmList
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback
                params = web.input()

                time = json.dumps( params.time )[1:-1]
                occurrence = json.dumps( params.occurrence )[1:-1]
                action = int( json.dumps( params.action )[1:-1] )

                print(occurrence)
                alarm = Alarm(time, action, occurrence)
                alarm.saveAlarm()

                return '%s(%s)' % (callbackName, alarmList.prettyAlarmList() )