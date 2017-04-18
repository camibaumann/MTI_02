import time
import os
import RPi.GPIO as GPIO
from twython import TwythonStreamer

# GPIO pin number of SERVO
SERVO = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT)
pwm = GPIO.PWM(SERVO,100)
pwm.start(5)

ss = ServoSix()

# Search terms
TERMS = '#trump, #immigration, #wall, #prolife #prochoice'

# Twitter application authentication
APP_KEY = 'GGjGahZ56kjEBLVXAUdllUWrO'
APP_SECRET = 'ksh52EBiJpxMv2ErSjlzwvlvwZsDQR6Zmo3PxZhjbNlC7CZpQL'
OAUTH_TOKEN = '3068198086-JkCcZtjOXtSM7iWqbZ4c0bmzjcu19KUoxdtMZcF'
OAUTH_TOKEN_SECRET = 'O9R97AXTqWbUqa8ANb8HMJQ4yylxowhcKeJXtgIPGpLov'

class ServoSix:
  servo_min = 500
  servo_max = 2500
    
  def __init__(self, servo_min=500, servo_max=2500):
    self.servo_min = servo_min
    self.servo_max = servo_max
    self.current_angle = servo_min
    # start the service
    os.system("sudo /etc/init.d/servoblaster start")
        
    
  def set_servo(self, angle):
    if angle < 0 or angle > 180:
        print("Angle 0 to 180")
    else:
        range = self.servo_max - self.servo_min
        scaler = range / 180
        pulse = self.servo_min + angle * scaler
        self.current_angle = self.servo_min + angle * scaler
        command = "echo {}={}us > /dev/servoblaster".format(6, pulse)
        os.system(command)
            
            
  def move_servo(self,  start_angle, end_angle, delay):
    inc = 1
    angle = start_angle
    if start_angle > end_angle:
      inc = -1
    while angle != end_angle:
      angle += inc
      self.set_servo(angle)
      time.sleep(delay)
            
  def cleanup(self):
    # stop the service
    os.system("sudo /usr/bin/killall servod")
    # disable it so it doesn't start after reboot'
    os.system("sudo update-rc.d servoblaster disable")  
        
# Setup callbacks from Twython Streamer
class Twitter2RaspberryPi(TwythonStreamer):
  def on_success(self, data):
    print "on success"
    if 'text' in data:
      # if 'immigration' in data:
      #   print data['text'].encode('utf-8')
      #   ss.move_servo(ss.current_angle, 50, 10)
      # elif 'prochoice' in data or 'prolife' in data: 
      #   print data['text'].encode('utf-8')
      ss.move_servo(ss.current_angle, 100, 10)

  def on_error(self, status_code, data):
    print status_code, data

# Create streamer
try:
  ss.set_servo(0):
  stream = Twitter2RaspberryPi(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
  stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
  GPIO.cleanup()
  ss.cleanup()

# root = Tk()
# root.wm_title('Servo Control')
# app = App(root)
# root.geometry("200x50+0+0")
# root.mainloop()


