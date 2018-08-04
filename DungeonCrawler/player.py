from guns import *
from tkinter import *
import math

#player initially has 3 health 
class Player (object):
    def __init__(self, name, x, y, angle):
        self.name = name
        self.health = 3
        self.currHealth = self.health
        self.bag = []
        self.guns = []
        self.equipped = []
        self.gun = "pistol"
        self.x = x
        self.y = y
        self.angle = angle
        self.r = 50
        self.img = PhotoImage(file="Images/player.gif")

    #changes the angle to face in the direction of event
    def changeAngle(self, event, data):
        x = self.x - event.x
        y = self.y - event.y
        if x==0 or y==0: return
        if x>0:
            self.angle = math.atan(y/x)+math.pi
        else:
            self.angle = math.atan(y/x)

    def move(self, dir, data):
        self.x += dir[0]
        self.y += dir[1]
        if self.x<self.r: self.x=self.r
        elif self.x>data.width-self.r: self.x = data.width-self.r
        if self.y<self.r: self.y=self.r
        elif self.y>data.height-self.r: self.y = data.width-self.r

    #the polygon makes a triangle point at cursor
    def draw(self, canvas):
        #creates a triangle pointing in the direction of the mouse
        angle = self.angle
        canvas.create_image(self.x-self.r, self.y-self.r, anchor=NW, image=self.img)
        canvas.create_polygon((self.x + self.r*math.cos(angle+math.pi/30), self.y + self.r*math.sin(angle+math.pi/30)),
                             (self.x + self.r*math.cos(angle-math.pi/30), self.y + self.r*math.sin(angle-math.pi/30)),
                             (self.x + (self.r+20)*math.cos(angle), self.y + (self.r+20)*math.sin(angle)))