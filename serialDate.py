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
		web.header('Content-Type', 'text/javascript')
		params = web.input()
		addRemoveAlarms.addAlarm( params.hour, params.minute )

		#Return the staged alarms back to the front end
		return json.dumps(addRemoveAlarms.alarmList)
		

if __name__ == "__main__":
	app = web.application(urls, globals() )
	app.run()