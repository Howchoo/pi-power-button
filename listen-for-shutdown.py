#!/usr/bin/env python
import RPi.GPIO as GPIO
import subprocess
import time

print('Raspberry PI GPIO Button & LED Shutdown Script')

# Pin Definitions
PIN_LED    = 4 # GPIO4 / Pin #7
PIN_BUTTON = 3 # GPIO3 / Pin #5

try:
    # Button Press Logic
    def button_interupt(channel):
        time_start = time.time()
        time_button = 0
        led_state = GPIO.LOW
        time_pressed_max = 3 # seconds

        # Loop while button is pressed, and not passed max time
        while GPIO.input(channel) == GPIO.LOW and time_button <= time_pressed_max: # wait for the button up
            # DEBUGGING OUTPUT
            print("Button:", time_button, led_state)

            # Blink LED
            GPIO.output(PIN_LED, led_state)  # blink LED
            led_state = not led_state
            time.sleep(0.1) #loop time and led blink interation rate.

            # How long was the button down?
            time_button = time.time() - time_start    

        # Set LED back to High, just in case was low.
        GPIO.output(PIN_LED, GPIO.HIGH)  # blink LED

        # Determine Button Time
        if time_button >= time_pressed_max:
            print("Power Button Pressed & Held:", time_button)
            subprocess.call(['shutdown', '-h', 'now'], shell=False) # Power Off

    # Ignore Warrnings or not
    GPIO.setwarnings(False)    # Ignore warning for now

    # Setting GPIO layout
    GPIO.setmode(GPIO.BCM)   # GPIO.setmode(gpio.BOARD) | Use boards header pin order or lableing GPIO##. https://iot4beginners.com/difference-between-bcm-and-board-pin-numbering-in-raspberry-pi/

    # # Set pin as input pin pulled down to GND
    GPIO.setup(PIN_LED, GPIO.OUT, initial=GPIO.HIGH)           # LED ON
    GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button

    # # Button Press Event
    GPIO.add_event_detect(PIN_BUTTON, GPIO.FALLING, callback=button_interupt, bouncetime=100)

    # Sleep Forever, to keep script alive, button_interupt handles everything.
    while True:
        time.sleep(86400)
except:
    GPIO.cleanup()
