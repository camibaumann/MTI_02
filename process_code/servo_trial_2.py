"""original code
http://www.toptechboy.com/raspberry-pi/raspberry-pi-
lesson-28-controlling-a-servo-on-raspberry-pi-with-python/
and "The Raspberry Pi Cookbook" by O'Reilly
modifications by Camille Baumann-Jaeger"""

import time
import os
from Tkinter import *
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)#sets servo signal pin at #12
pwm = GPIO.PWM(12,100)#creates PWM object on Pin 12 with a 100Hz signal
pwm.start(5) #sets servo to full left position

