"""original code from "The Raspberry Pi Cookbook" by O'Reilly
modified by Camille Baumann-Jaeger

some changes made off of lessons on 
http://www.toptechboy.com/raspberry-pi/raspberry-pi-
lesson-28-controlling-a-servo-on-raspberry-pi-with-python/
notes: 
1)All comments are by Camille Baumann-Jaeger"""


import time
import os
from Tkinter import *
import RPi.GPIO as GPIO

##scp  '/cygdrive/c/Users/Camille/Documents/MakingThingsInteractive/Project 02/code/servo_cami.py' pi@128.237.237.94:~/

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)#sets servo signal pin at #12
pwm = GPIO.PWM(12,100)#creates PWM object on Pin 12 with a 100Hz signal
pwm.start(5) #sets servo to full left position

class ServoSix:
    
    servo_min = 500
    servo_max = 2500
    
    def __init__(self, servo_min=500, servo_max=2500):
        self.servo_min = servo_min
        self.servo_max = servo_max
        # start the service
        os.system("sudo /etc/init.d/servoblaster start")
        
    
    def set_servo(self, servo, angle):
        if servo < 1 or servo > 6:
            print("Servo 1 to 6")
        elif angle < 0 or angle > 180:
            print("Angle 0 to 180")
        else:
            range = self.servo_max - self.servo_min
            scaler = range / 180
            pulse = self.servo_min + angle * scaler
            command = "echo {}={}us > /dev/servoblaster".format(servo, pulse)
            os.system(command)
            
            
    def move_servo(self, servo, start_angle, end_angle, delay):
        inc = 1
        angle = start_angle
        if start_angle > end_angle:
            inc = -1
        while angle != end_angle:
            if angle==0 or angle==90 or angle==180:
                angle += inc
                self.set_servo(servo, angle)
                time.sleep(delay)
            else:
                return 
                
    def cleanup(self):
        # stop the service
        os.system("sudo /usr/bin/killall servod")
        # disable it so it doesn't start after reboot'
        os.system("sudo update-rc.d servoblaster disable")	
        
class App:
    
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        scale = Scale(frame, from_=0, to=180,
            orient=HORIZONTAL, command=self.update)
        scale.grid(row=0)
        
    def update(self, angle):
        duty = float(angle) / 10.0 + 2.5
        pwm.ChangeDutyCycle(duty)
        
root = Tk()
root.wm_title('Servo Control')
app = App(root)
root.geometry("200x50+0+0")
root.mainloop()

ss = ServoSix()

