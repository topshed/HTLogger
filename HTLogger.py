from astro_pi import AstroPi
import time
import logging
from datetime import datetime
import TwoDigitGrid as TDG

ap = AstroPi()

dataWriteInterval = 120                           # how often data is written to file (seconds)
dataDisplayInterval = 0.5                         # how often the displayed value is updated (seconds)

tmstmp = time.strftime("%Y%m%d-%H%M%S")           # Set timestamp format for the logging filename
logging.basicConfig(format='%(asctime)s %(message)s',filename='readings'+str(tmstmp)
+'.log',level=logging.DEBUG)                      # set up logging

hum_prev = 0                                      # set previous humidity and temp values to zero
temp_prev = 0
sec_count = 0

while True:                                       # Main program loop

	x, y, z = ap.get_accelerometer_raw().values() #Get raw accelerometer values and round them
	x = round(x, 0)
	y = round(y, 0)
	temp_f = ap.get_temperature()                 # Get temperature from astro-pi
	hum_f = ap.get_humidity()                     # Get humidity from astro-pi
	hum_int = int(hum_f)                          # convert to integers
	temp_int = int(temp_f)

	if (sec_count >= dataWriteInterval/dataDisplayInterval) or (sec_count == 0): 
		logging.info('humidity: ' + str(hum_f) + ' temperature: ' + str(temp_f))
		sec_count = 0

	if x == -1 and y != -1:                        # humidity display if HDMI port pointing upwards
		ap.set_rotation(270)
		if hum_int > hum_prev:                     # Is the latest reading higher than the last?
			r = [0,255,0]                          # green if higher
		elif hum_int == hum_prev:
			r = [0,0,255]                          # blue if the same
		else:
			r = [0,255,255]                        # light blue if lower
		hum_prev = hum_int
		image=TDG.numToMatrix(hum_int,back_colour=[0,0,0],text_colour=r)
		ap.set_pixels(image)
	elif y == -1 and x != -1:                      # temp display if USB ports pointing upwards
		ap.set_rotation(180)
		if temp_int > temp_prev:                   # Is the latest reading higher than the last?
			r = [255,0,0]                          # red if higher
		elif temp_int == temp_prev:
			r = [255,128,0]                        # orange if the same
		else:
			r = [255,215,0]                        # yellow if lower
		temp_prev = temp_int
		# use numToMatrix to turn the number into a 64 item list suitable for the LED
		image=TDG.numToMatrix(temp_int,back_colour=[0,0,0],text_colour=r)
		ap.set_pixels(image)
	elif x == 0 and y == 0:                        # if the Pi is flat on its back
		ap.show_message("Recording", text_colour=[150,150,150],scroll_speed=0.03) 
	else:
		ap.show_letter("?")                       # display a ? if at some other orientation

	time.sleep(dataDisplayInterval)
	sec_count+=1



