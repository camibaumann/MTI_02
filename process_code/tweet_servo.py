import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer

# Search terms
TERMS = '#trump, #immigration'

# GPIO pin number of LED
LED = 22

# Twitter application authentication
APP_KEY = 'GGjGahZ56kjEBLVXAUdllUWrO'
APP_SECRET = 'ksh52EBiJpxMv2ErSjlzwvlvwZsDQR6Zmo3PxZhjbNlC7CZpQL'
OAUTH_TOKEN = '3068198086-JkCcZtjOXtSM7iWqbZ4c0bmzjcu19KUoxdtMZcF'
OAUTH_TOKEN_SECRET = 'O9R97AXTqWbUqa8ANb8HMJQ4yylxowhcKeJXtgIPGpLov'


# Setup callbacks from Twython Streamer
class Twitter2RaspberryPi(TwythonStreamer):
  def on_success(self, data):
    print "on success"
    if 'text' in data:
      print data['text'].encode('utf-8')
      GPIO.output(LED, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(LED, GPIO.LOW)

  def on_error(self, status_code, data):
        print status_code, data

# Setup GPIO as output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

# Create streamer
try:
  stream = Twitter2RaspberryPi(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  print "streaming"
  stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
  GPIO.cleanup()
