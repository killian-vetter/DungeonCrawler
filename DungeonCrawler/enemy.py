from guns import *
from tkinter import *
import random
import math

def getAngle(x, y, data):
    x = x - data.player.x
    y = y - data.player.y
    if x>0:
        angle = math.atan(y/x)+math.pi
    else:
        angle = math.atan(y/x)
    return angle

#this basic type of enemy takes 3 hit from a pistol and follows you and shoots straight at you
class Enemy (object):
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.health = 6
        self.h = 150
        self.w = 75
        self.img = PhotoImage(file="Images/enemy.gif")
        self.angle = 0
        self.lifeTime = random.randint(0,50)

    def shoot(self, data):
        data.enemyBullets.append(Bullet(self.x, self.y, 15, self.angle, "red", 10, 1))

    def move(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)

    #sets the angle to point at player. Moves toward player.
    #Shoots at player every 2 seconds
    def onTimerFired(self, data):
        self.lifeTime += 1
        self.angle = getAngle(self.x, self.y, data)
        if self.lifeTime % 20 == 0:
            self.shoot(data)
        self.move()
   
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, anchor=NW, image=self.img)

class MachineGunEnemy (Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = PhotoImage(file="Images/machineGun.gif")

    def onTimerFired(self, data):
        self.lifeTime += 1
        self.angle = getAngle(self.x, self.y, data)
        if self.lifeTime % 8 == 0:
            self.shoot(data)
        self.move()

class Shotgun (Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = PhotoImage(file="Images/shotgun.gif")

    def shoot(self, data):
        super().shoot(data)
        data.enemyBullets.append(Bullet(self.x, self.y, 15, self.angle+math.pi/18, "red", 10, 1))
        data.enemyBullets.append(Bullet(self.x, self.y, 15, self.angle-math.pi/18, "red", 10, 1))

class BigEnemy1 (Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.helth = 10
        self.r = 100
        self.w = 0
        self.h = 0
        self.speed = 0
        self.angle = (random.random())*math.pi/7
        self.img = PhotoImage(file="Images/bigEnemy1.gif")

    def onTimerFired(self, data):
        x = self.x+self.r
        y = self.y+self.r
        self.angle += math.pi/5
        data.enemyBullets.append(Bullet(x+self.r*math.cos(self.angle), 
                                        y+self.r*math.sin(self.angle),
                                        15, self.angle, "red", 10, 1))