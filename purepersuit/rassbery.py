# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/
import math
import pygame
from Vec2d import Vec2d
from purepersuit import Vehicle
pygame.init()

import RPi.GPIO as GPIO          
import time 

in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
servo=17
GPIO.setup(servo,GPIO.OUT)
servo1 = GPIO.PWM(servo,50)
servo1.start(0)

def angle(Vehicle.self.theta):
    angle1 = Vehicle.update()
    servo1.ChangeDutyCycle(2+(angle1/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(2)
    


p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run f-forward s-stop e-exit")
print("\n")    
duty=2
while(1):
    
    angle()
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p.ChangeDutyCycle(75)
    servo1.ChangeDutyCycle(2)
    print("forward")
    
    p.ChangeDutyCycle(20)
    p.ChangeDutyCycle(10)
    servo1.ChangeDutyCycle(4)
    print('turn 45')
    servo1.ChangeDutyCycle(2)
        
    p.ChangeDutyCycle(20)
    
    p.ChangeDutyCycle(10)
    servo1.ChangeDutyCycle(4)
    print('turn 45')
   
    servo1.ChangeDutyCycle(2)
   
        
    p.ChangeDutyCycle(20)
    
    p.ChangeDutyCycle(10)
    servo1.ChangeDutyCycle(4)
    print('turn 45')
    
    servo1.ChangeDutyCycle(2)
   
    
    p.ChangeDutyCycle(20)
    
    p.ChangeDutyCycle(10)
    servo1.ChangeDutyCycle(4)
    print('turn 45')
    
    servo1.ChangeDutyCycle(2)
 
    
    
    
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
        
        
     
    
    p.stop()
    GPIO.cleanup()
    print("GPIO Clean up")
    break
    
   
    print("<<<  wrong data  >>>")
    print("please enter the defined data to continue.....")


