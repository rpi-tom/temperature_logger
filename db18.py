#!/usr/bin/env python

import os
import time
from datetime import datetime

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#28-011453d885aa
temp_sensor_1 = '/sys/bus/w1/devices/28-0114543d8eaa/w1_slave'
temp_sensor_2 = '/sys/bus/w1/devices/28-01145a874581/w1_slave'
temp_sensor_3 = '/sys/bus/w1/devices/28-01145e853df5/w1_slave'


def read_temp_raw(id):
	temp_sensor_location = id
	f = open(temp_sensor_location, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp(id):

	lines = read_temp_raw(id)
	while lines[0].strip()[-3:] != 'YES':
		sleep(0.2)
		lines = read_temp_raw()
	temp_result = lines[1].find('t=')

	if temp_result != -1:
		temp_string = lines[1].strip()[temp_result + 2:]
		# Temperature in Celcius
		temp = float(temp_string) / 1000.0
		# Temperature in Fahrenheit
		#temp = ((float(temp_string) / 1000.0) * (9.0 / 5.0)) + 32.0
		return temp

while True:
	now = datetime.now()
	ts = now.strftime("%Y-%m-%d.%H:%M:%S")
	id = int(time.time())
	temperature = []
	t = now.strftime("%Y-%m-%d")
	for x in range(1,4):
		sens_id = eval("temp_sensor_" + str(x))
		temperature.append(read_temp(sens_id))
		#print(x,": ",read_temp(sens_id))
		time.sleep(0.5)
	line = "{0},{1},{2:.3f},{3:.3f},{4:.3f} \n" .format(ts,id,temperature[0],temperature[1],temperature[2])
	filename =  "/home/pi/temp_data/readings_"+ str(t)+".csv"
	with open(filename,'a') as fd:
		fd.write(line)
	#diagnostic = "T1: "+ str(temperature[0]) + " T2: "+ str(temperature[1]) + " T3: " + str(temperature[2])
	###use this to print temperature onto the screen###
	#print (diagnostic)
	time.sleep(60)
