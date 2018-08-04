from guns import *
from tkinter import *

def getAngle(x, y, data):
    x = x - data.player.x
    y = y - data.player.y
    if x>0:
        angle = math.atan(y/x)+math.pi
    else:
        angle = math.atan(y/x)
    return angle

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
        self.lifeTime = 0

    def shoot(self, data):
        data.enemyBullets.append(Bullet(self.x, self.y, 20, self.angle, "red", 10, 1))

    def move(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)

    def onTimerFired(self, data):
        self.lifeTime += 1
        self.angle = getAngle(self.x, self.y, data)
        if self.lifeTime % 10 == 0:
            self.shoot(data)
        self.move()
   
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, anchor=NW, image=self.img)
