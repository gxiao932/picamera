﻿#!/usr/bin/env python

from picamera import PiCamera
import time
import os
import shutil
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

DEBUG = False
camera = PiCamera()

imageName = '/mnt/vincent/images/recent.jpg'
root = '/home/pi/images/'
var = 1
delay = 60
lastTime = time.strftime('%m-%d-%y-%H:%M:%S')
firstDate = time.strftime('%m-%d-%y')
rotate = 180
tm = time.strftime('%H')
dateList = os.listdir('/home/pi/images')
difference = True
length = len(dateList)
oldestDate = 991231
 
#deletes things now
def DeleteOldest():
	global oldestDate
	global difference

	while difference:
		difference = False

		for i in range (0, length):
			string = dateList[i].split('-')
			currentDate = int(string[2] + string[0] + string [1])

			if currentDate < oldestDate:
				oldestDate = currentDate
				difference = True

	finalDate = str(oldestDate)
	finalDate = list(finalDate)

	deleteName = finalDate[2] + finalDate[3] + '-'+ finalDate[4] + finalDate[5] + '-' + finalDate[0] + finalDate[1]
	shutil.rmtree(root+'/'+deleteName)




while True:

	date = time.strftime('%m-%d-%y')
	st = os.statvfs('/')

	if not os.path.exists(root+date):
		os.makedirs(root+date)

	time.sleep(delay)

	if 5 < tm < 12:
		tm = time.strftime('%H')
		currTime = time.strftime('%m-%d-%y-%H:%M:%S')
		archiveName = root+date+'/'+'image-'+currTime+'.jpg'
		camera.capture(archiveName)

		img = Image.open(archiveName)
		img = img.rotate(rotate)
		draw = ImageDraw.Draw(img)
		font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 20)
		draw.text((0,0), currTime, (255,255,255), font = font)
		img.save(archiveName)

		try:
			shutil.copy2(archiveName, imageName)
		except IOError:
			break

		lastTime = 'image' + currTime
		#var += 1

		if st.f_bavail < 24414:
			DeleteOldest()
