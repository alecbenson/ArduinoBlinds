#!/usr/bin/python3

from serial import Serial
import glob
import sys
import time

#Auto detect port if possible, otherwise ask user
port = glob.glob("/dev/ttyACM*")
if len(port) <= 0:
	port = raw_input("No port could be found. If you know the correct port, enter it:")
elif len(port) > 1:
	print port
	port = raw_input("More than one valid port has been found. Which should we use:")
else:
	print("Autodetected port " + port[0])
	port = port[0]
	

ser = Serial(port, 9600, timeout=1)
print("Successfully connected to: " + ser.portstr)

while True:
	print(time.time())
	ser.write( str(time.time()).encode() )
	time.sleep(20000)
