#!/usr/bin/env python

import signal
import sys
import RPi.GPIO as GPIO
import subprocess
import time

PWR_BUTTON_GPIO = 3     # 9(GND) 5-GPIO3(+)
RST_BUTTON_GPIO = 4     # 9(GND) 7-GPIO4(+)
LED_STATUS_GPIO = 18    # 6(GND) 12-GPIO18(+)
DEBOUNCE_TIME = 300

# DEBUG
# if __name__ == '__main__':
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(PWR_BUTTON_GPIO, GPIO.IN)
#     pressed = False
#     while True:
#         # button is pressed when pin is LOW
#         if not GPIO.input(PWR_BUTTON_GPIO):
#             print("Button pressed!")
#         else:
#             print("Button not pressed!")
#         time.sleep(0.5)

def signal_handler(sig, frame):
    # print("Cleanup and exit...")
    GPIO.cleanup()
    sys.exit(0)

def button_power_pressed_callback(channel):
    # print("POWER BUTTON PRESSED!")
    subprocess.call(['shutdown', '-h', 'now'], shell=False)

def button_reboot_pressed_callback(channel):
    # print("REBOOT BUTTON PRESSED!")
    subprocess.call(['shutdown', '-r', 'now'], shell=False)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(LED_STATUS_GPIO, GPIO.OUT)
    GPIO.setup(PWR_BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RST_BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.output(LED_STATUS_GPIO, GPIO.HIGH)
    GPIO.add_event_detect(PWR_BUTTON_GPIO, GPIO.FALLING, callback=button_power_pressed_callback, bouncetime=DEBOUNCE_TIME)
    GPIO.add_event_detect(RST_BUTTON_GPIO, GPIO.FALLING, callback=button_reboot_pressed_callback, bouncetime=DEBOUNCE_TIME)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
