# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
from twython import TwythonStreamer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA

# Search terms
TERMS = 'trump immigration, trump immigrants, trump wall, trump women, trump prolife, trump prochoice, trump security, trump defence'

# Twitter application authentication
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# Import the PCA9685 module.
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 600  # Min pulse length out of 4096
servo_immigration = 1000 # Max pulse length out of 4096
servo_women = 2000
servo_tech = 2500

sid = SIA()

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(self, channel, pulse):
  pulse_length = 1000000    # 1,000,000 us per second
  pulse_length //= 60       # 60 Hz
  print('{0}us per period'.format(pulse_length))
  pulse_length //= 4096     # 12 bits of resolution
  print('{0}us per bit'.format(pulse_length))
  pulse *= 1000
  pulse //= pulse_length
  pwm.set_pwm(channel, 0, pulse)
  # Set frequency to 60hz, good for servos.
  pwm.set_pwm_freq(60)

class Servo(object): 
  def move_servo(self, channel):
    if (channel == -1): 
      pwm.set_pwm(0, 0, servo_min)
    elif (channel == 0):
    # Move servo on channel O between extremes.
        pwm.set_pwm(0, 0, servo_immigration)
        time.sleep(3)
        pwm.set_pwm(0, 0, servo_min)
    elif (channel == 1):
        pwm.set_pwm(0, 0, servo_women)
        time.sleep(3)
        pwm.set_pwm(0, 0, servo_min)
    else: 
        pwm.set_pwm(0, 0, servo_tech)
        time.sleep(3)
        pwm.set_pwm(0, 0, servo_min)


servo = Servo()

class Twitter2RaspberryPi(TwythonStreamer):
  def on_success(self, data):
    if 'text' in data:
      text_body = data['text']
      ss = sid.polarity_scores(text_body)
      print ss["compound"], ss["neg"]
      #print (('{0}: {1}, ').format(k, ss[k]), end='')
      if (ss["compound"] < -0.5):
        if 'immigration' in text_body or 'immigrants' in text_body or 'wall':
            print "IMMIGRATION"
            print data['text'].encode('utf-8')
            servo.move_servo(0)
            time.sleep(0.5)
        elif 'women' in text_body or 'prolife' in text_body:
            print "WOMEN"
            print data['text'].encode('utf-8')
            servo.move_servo(1)
            time.sleep(0.5)
        elif 'security' in text_body or 'defence' in text_body:
            print "security/defence"
            print data['text'].encode('utf-8')
            servo.move_servo(1)
            time.sleep(0.5)

  def on_error(self, status_code, data):
    print status_code, data

# Create streamer
try:
  #servo.move_servo(-1)
  stream = Twitter2RaspberryPi(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
  print "we out"