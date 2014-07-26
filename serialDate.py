#usr/bin/python3

from serial import Serial
import glob
import sys
import time
import datetime
import web

urls = (
	'/', 'index'
)

class index:
	def GET(self):
		web.header('Content-Type', 'text/javascript')
		params = web.input()
		return serialWrite( params.hour, params.minute )
		

if __name__ == "__main__":
	app = web.application(urls, globals() )
	app.run()

def serialWrite(hour, minute):
	port = glob.glob("/dev/ttyACM*")
	print("Autodetected port " + port[0])
	port = port[0]
			
	ser = Serial(port, 9600, timeout=1)
	print("Successfully connected to: " + ser.portstr)
	
	ser.write('a')
	print(hour + ":" + minute);
	return "console.log('ALARM SET FOR: ' + " + hour + "+ ':' +" + minute + ");"

