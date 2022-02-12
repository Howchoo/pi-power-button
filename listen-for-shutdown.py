#!/usr/bin/env python


import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

stay=1 #incidcates if shutdown hasbeen sent correctly

while stay:
	GPIO.wait_for_edge(3, GPIO.FALLING) #button is pressed
	for i in range(30): #wait for a second
		time.sleep(0.1)
		if GPIO.input(3) == 1: #if button not pressed
			stay=1
			break
		else:
			stay=0

subprocess.call(['shutdown', '-h', 'now'], shell=False)
