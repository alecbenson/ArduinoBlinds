#usr/bin/python3
import sys
import web
import json
from alarm import Alarm
from alarmList import AlarmList

urls = (
        '/', 'GetAlarms',
        '/add', 'Add',
        '/toggle', 'Toggle',
        '/remove', 'Remove'
        )

alarmList = AlarmList(60)
alarmList.check() #check for triggerable alarms

#handles the web service
class Toggle:
        def GET(self):
                global alarmList
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback

                #Return the staged alarms back to the front end
                return '%s(%s)' % (callbackName, alarmList.prettyAlarmList() )

class GetAlarms:
        def GET(self):
                global alarmList
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback

                #Return the staged alarms back to the front end
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

                #Parse our json and remove the quotation marks at the begining and end
                time = json.dumps( params.time )[1:-1]
                repeat = int( json.dumps( params.repeat )[1:-1] )
                action = int( json.dumps( params.action )[1:-1] )

                alarm = Alarm(time, action, repeat)
                alarmList.add(alarm)
                dalist = ['this','test']

                #Return the staged alarms back to the front end
                return '%s(%s)' % (callbackName, alarmList.prettyAlarmList() )

if __name__ == "__main__":
        app = web.application(urls, globals() )
        app.run()