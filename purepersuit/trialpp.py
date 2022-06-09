import math
import pygame
from Vec2d import Vec2d
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
p.start(15)
servo1.ChangeDutyCycle(2)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run f-forward s-stop e-exit")
print("\n")


done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
mouseX = 0
mouseY = 0
drawing = []

ratio = 10
numbers = 40

size = ratio * numbers
screen = pygame.display.set_mode([size*2, size])
pygame.display.set_caption("Path Following")
clock = pygame.time.Clock()


def show_drawing():
    pygame.draw.circle(screen, BLUE,  [drawing[0].x, drawing[0].y], 10)
    for i in range(drawing.__len__()-1):
        pygame.draw.line(screen, WHITE, [drawing[i].x, drawing[i].y], [drawing[i+1].x, drawing[i+1].y])


def set_target():
    while drawing[0].distance(vehicle.pos) < ld:
        if len(drawing) == 1:
            break
        drawing.pop(0)
def degree(x):
        x=math.degrees(x)
        return x
    
def angle(theta):
    angle1 = theta
    if angle1 > 15:
        angle1=15
    elif angle1 < -15:
        angle1=-15
    else:
        angle1=angle1
        
    print('Duty Cycle',(2+(angle1/18)))
    return (2+(angle1/18))

def servo(duty):
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p.ChangeDutyCycle(15)
    servo1.ChangeDutyCycle(duty)

class Vehicle:
    def __init__(self, x, y):
        self.pos = Vec2d(x, y)
        self.vel = 0.5
        self.acc = 0
        self.theta = 0
        self.delta = 0
        self.alpha = 0
        self.length = 100
        self.kaapa = 0
        self.desired = 0.1
        self.ld = 0

    def update(self):
        if self.delta > 1:
            self.delta = 1
        elif self.delta < -1:
            self.delta = -1
        self.vel += self.acc
        self.pos.x += self.vel * math.cos(-self.theta)
        self.pos.y += self.vel * math.sin(-self.theta)
        self.theta += self.vel * (math.tan(self.delta) / self.length)
        print("Value in Degree:",degree(self.theta))
        ang=degree(self.theta)
        duty=angle(ang)
        servo(duty)
   

    def seek_2(self, point):
        self.ld = self.pos.distance(point)
        self.alpha = (drawing[0].sub_vect(Vec2d(self.pos.x - self.length * math.cos(-self.theta), self.pos.y - self.length * math.sin(-self.theta)))).angle() - self.theta
        self.kaapa = (2 * math.sin(self.alpha)) / self.ld
        if math.atan2(self.kaapa * self.length, 1) - self.delta > 0.02:
            self.delta += 0.03
        elif self.delta - math.atan2(self.kaapa * self.length, 1) > 0.02:
            self.delta -= 0.03

    def show_vehicle(self):
        pygame.draw.polygon(screen, GREEN, rect(self.pos.x + (self.length/2) * math.cos(-self.theta),
                                                self.pos.y + (self.length/2) * math.sin(-self.theta),
                                                -self.theta, self.length, 10))
        pygame.draw.polygon(screen, RED, rect(self.pos.x + self.length * math.cos(-self.theta),
                                              self.pos.y + self.length * math.sin(-self.theta),
                                              -self.delta - self.theta, 40, 17))
        pygame.draw.polygon(screen, RED, rect(self.pos.x, self.pos.y,  -self.theta, 40, 17))


def rect(x, y, angle, w, h):
    return [translate(x, y, angle, -w/2,  h/2),
            translate(x, y, angle,  w/2,  h/2),
            translate(x, y, angle,  w/2, -h/2),
            translate(x, y, angle, -w/2, -h/2)]


def translate(x, y, angle, px, py):
    
    x1 = x + px * math.cos(angle) - py * math.sin(angle)
    y1 = y + px * math.sin(angle) + py * math.cos(angle)
   
    return [x1, y1]


vehicle = Vehicle(100, size-100)
ld = 150

while not done:

    clock.tick(80)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    if pygame.mouse.get_pressed()[0]:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        print('position',mouseX, mouseY)
        if not len(drawing):
            drawing.append(Vec2d(mouseX, mouseY))
        if not drawing[-1].x == mouseX and not drawing[-1].y == mouseY:
            drawing.append(Vec2d(mouseX, mouseY))

    if len(drawing):
        show_drawing()
        set_target()
        vehicle.seek_2(drawing[0])

    vehicle.update()
    vehicle.show_vehicle()
    pygame.display.flip()

pygame.quit()

servo1.ChangeDutyCycle(2)
p.stop()
GPIO.cleanup()
print("GPIO Clean up")