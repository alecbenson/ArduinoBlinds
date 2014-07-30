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
alarmList.check() #check for triggerable alarms

#handles the web service
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

class GetAlarms:
        def GET(self):
                global alarmList
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback
                return '%s(%s)' % (callbackName, alarmList.prettyAlarmList() )

class Remove:
        def GET(self):
                global alarmList
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback
                params = web.input()
                index = int( json.dumps( params.index )[1:-1] )
                alarmList.remove( index )
                return '%s(%s)' % (callbackName, alarmList.prettyAlarmList() )

class Add:
        def GET(self):
                global alarmList
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback
                params = web.input()

                time = json.dumps( params.time )[1:-1]
                repeat = int( json.dumps( params.repeat )[1:-1] )
                action = int( json.dumps( params.action )[1:-1] )

                alarm = Alarm(time, action, repeat)
                alarmList.add(alarm)
                dalist = ['this','test']

                return '%s(%s)' % (callbackName, alarmList.prettyAlarmList() )

if __name__ == "__main__":
        app = web.application(urls, globals() )
        app.run()