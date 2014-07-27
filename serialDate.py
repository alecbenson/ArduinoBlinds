#usr/bin/python3

import addRemoveAlarms
import sys
import web
import json

urls = (
        '/', 'index'
)

#starts the alarm checking thread
addRemoveAlarms.checkTime()

#handles the web service
class index:
        def GET(self):
                web.header('Content-Type', 'application/javascript')
                callbackName = web.input(callback='callback').callback
                params = web.input()

                #Parse our json and remove the quotation marks at the begining and end
                time = json.dumps( params.time )[1:-1]
                repeat = int( json.dumps( params.repeat )[1:-1] )
                action = int( json.dumps( params.action )[1:-1] )
                addRemoveAlarms.addAlarm( time, action, repeat)

                #Return the staged alarms back to the front end
                return '%s(%s)' % (callbackName, addRemoveAlarms.alarmList)


if __name__ == "__main__":
        app = web.application(urls, globals() )
        app.run()
