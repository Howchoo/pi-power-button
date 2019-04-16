#!/usr/bin/env python


from gpiozero import Button
import subprocess

button = Button(3)

button.wait_for_press()

subprocess.call(['shutdown', '-h', 'now'], shell=False)
