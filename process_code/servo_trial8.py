import time
import os
from Tkinter import *
import RPi.GPIO as GPIO
from twython import TwythonStreamer


GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12,100)
pwm.start(5)


# Search terms
TERMS = '#trump, #immigration'

# GPIO pin number of LED
LED = 22

# Twitter application authentication
APP_KEY = 'GGjGahZ56kjEBLVXAUdllUWrO'
APP_SECRET = 'ksh52EBiJpxMv2ErSjlzwvlvwZsDQR6Zmo3PxZhjbNlC7CZpQL'
OAUTH_TOKEN = '3068198086-JkCcZtjOXtSM7iWqbZ4c0bmzjcu19KUoxdtMZcF'
OAUTH_TOKEN_SECRET = 'O9R97AXTqWbUqa8ANb8HMJQ4yylxowhcKeJXtgIPGpLov'

tweet_count=0

# Setup callbacks from Twython Streamer
class Twitter2RaspberryPi(TwythonStreamer):
  nonlocal tweet_count
  def on_success(self, data, count=0):
    print "on success"
    if 'text' in data:
      print data['text'].encode('utf-8')
      tweet_count+=1
      GPIO.output(12, GPIO.HIGH)

  def on_error(self, status_code, data):
        print status_code, data

# Create streamer
try:
  stream = Twitter2RaspberryPi(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  print "streaming"
  stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
  GPIO.cleanup()


servo_min = 500
servo_max = 2500
            
def set_servo(servo, angle):
    if servo < 1 or servo > 6:
        print("Servo 1 to 6")
    elif angle < 0 or angle > 180:
        print("Angle 0 to 180")
    else:
        range = self.servo_max - servo_min
        scaler = range / 180
        pulse = servo_min + angle * scaler
        command = "echo {}={}us > /dev/servoblaster".format(servo, pulse)
        os.system(command)
            
            
def move_servo(servo, start_angle, end_angle, delay):
    inc = 1
    angle = start_angle
    if start_angle > end_angle:
       inc = -1
    while angle != end_angle:
        angle += inc
        self.set_servo(servo, angle)
        time.sleep(delay)
            
def cleanup(self):
    # stop the service
    os.system("sudo /usr/bin/killall servod")
    # disable it so it doesn't start after reboot'
    os.system("sudo update-rc.d servoblaster disable")	
        
def update(self, angle):
   if tweet_count==7:
      angle=130
   if tweet_count==20:
      angle=90
   else: 
      duty = float(angle) / 10.0 + 2.5
      pwm.ChangeDutyCycle(duty)      

root = Tk()
root.wm_title('Servo Control')
app = App(root)
root.geometry("200x50+0+0")
root.mainloop()

ss = ServoSix()

