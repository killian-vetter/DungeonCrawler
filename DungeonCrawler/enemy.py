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
        self.health = 6
        self.h = 150
        self.w = 75
        self.img = PhotoImage(file="Images/enemy.gif")

    def shoot(self, data):
        angle = getAngle(self.x, self.y, data)
        data.enemyBullets.append(Bullets(x, y, 40, angle, "red", 10))
   
    def draw(self, canvas):
        canvas.create_image(self.x-self.w//2, self.y-self.h//2, anchor=NW, image=self.img)
