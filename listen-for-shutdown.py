#!/usr/bin/env python

import RPi.GPIO as GPIO
import subprocess
import time
from time import sleep

gpio_pin=3
long_press=30

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main():
  while True:
    GPIO.wait_for_edge(gpio_pin, GPIO.FALLING)
    counter = 0
    while GPIO.input(gpio_pin) == 0 and counter < long_press:
      time.sleep(0.1)
      counter += 1
      print('Shutdown button is pressed ' + str(counter))
    if counter >= long_press:
      print('Shutting down')
      subprocess.call(['shutdown', '-h', 'now'], shell=False)

if __name__ == '__main__':
  main()
