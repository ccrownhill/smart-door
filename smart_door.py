#!/usr/bin/python3

import face_recognition as fr
import numpy as np
from PIL import Image
from RPi import GPIO as gpio
import subprocess as sub
import lcddriver
import time

# set boolean whether the door is closed
global closed
closed = True
# set boolean whether the door can be opened
global openable
openable = True
# set up the lcd display in order to communicate with the enterer
lcd = lcddriver.lcd()
lcd.lcd_clear()
def reset_lcd():
	lcd.lcd_clear()
	lcd.lcd_display_string("Click the button", 1)
	lcd.lcd_display_string("Look into camera", 2)
reset_lcd()

# loading an image of me into ram
# so that picture of the one who wants to enter can be compared to it
me = Image.open("(put the path to an image of you here so that you can be recognized)")
me = me.resize((600, 600), Image.ANTIALIAS)
me = me.convert('RGB')
me = np.array(me)
me_enc = fr.face_encodings(me)[0]

# add another person to be recognized
# if you don't want anyone else to be recognized you can also remove this other person from the script
other = Image.open("(path to image of other person you want to be recognized)")
other = h.resize((600, 600), Image.ANTIALIAS)
other = h.convert('RGB')
other = np.array(h)
other_enc = fr.face_encodings(h)[0]

# provide functionality for opening the door
def open():
	global closed
	gpio.setup(relais, gpio.OUT)
	closed = False
	print("opening")

# provide functionality for closing the door
def close(x):
	gpio.remove_event_detect(outside)
	global closed
	global openable
	reset_lcd()
	if closed:
		# opening so the person from inside
		# can get out without any message
		# to the lcd display
		gpio.setup(relais, gpio.OUT)
	else:
		# closing door from the inside
		openable = False
		gpio.setup(relais, gpio.IN)
	closed = not closed
	if x == "not important":
		print("outside")
	print("closing")
	gpio.add_event_detect(outside, gpio.RISING, callback=try_access, bouncetime=10000)

# compare the face of the enterer to you
def compare(file):
	print("Comparing")
	img = Image.open(file)
	img = img.resize((600, 600), Image.ANTIALIAS)
	img = img.convert('RGB')
	img = np.array(img)
	enc = fr.face_encodings(img)[0]
	res = fr.compare_faces([me_enc, other_enc], enc)
	return (res[0] or res[1])

# take a pic of enterer
# compare it
# if its fine open the door
# the x parameter is only there because this one will be
# hooked up to gpio detect func which gives the pin number
# as a param for the callback func
def try_access(x):
	print("try")
	gpio.remove_event_detect(inside)
	global closed
	global openable
	if closed:
		if not openable:
			gpio.add_event_detect(inside, gpio.RISING, callback=close, bouncetime=4000)
			return
		sub.run("./photo.sh")
		try:
			if compare("(path to image file where take_pic.sh puts it)"):
				lcd.lcd_clear()
				lcd.lcd_display_string("Access granted",1)
				print("Access granted")
				open()
			else:
				lcd.lcd_clear()
				lcd.lcd_display_string("Access denied",1)
				time.sleep(1.5)
				reset_lcd()
				print("Access denied")
		except IndexError:
			lcd.lcd_clear()
			lcd.lcd_display_string("Face not", 1)
			lcd.lcd_display_string("recognizible", 2)
			time.sleep(1.5)
			reset_lcd()
			print("Please try again as the face was not recognizible")
	else:
		close("not important")
		openable = True
	gpio.add_event_detect(inside, gpio.RISING, callback=close, bouncetime=4000)
# setup the gpio configurations so the enterer can tell
# that he wants to enter by pressing a button
gpio.setmode(gpio.BCM)

# some gpio pins have bin damaged but 14,17,18,27 seem to work properly
gpio.setup(14, gpio.OUT)
gpio.setup(17, gpio.OUT)

inside = 8
outside = 12
gpio.setup(outside, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(inside, gpio.IN, pull_up_down=gpio.PUD_DOWN)

gpio.output(14, True)
gpio.output(17, True)

# setup pin 23 for controlling the relais which will switch the lock
# on and of
relais = 26

gpio.add_event_detect(inside, gpio.RISING, callback=close, bouncetime=4000)
gpio.add_event_detect(outside, gpio.RISING, callback=try_access, bouncetime=10000)

print("done")
try:
	while True:
		pass
except KeyboardInterrupt:
	gpio.cleanup()
	lcd.lcd_clear()
	print("over")
