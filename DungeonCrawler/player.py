from guns import *
from tkinter import *
import math

class Player (object):
    def __init__(self, name, x, y, angle):
        self.name = name
        self.health = 3
        self.currHealth = 3
        self.bag = []
        self.guns = []
        self.equipped = []
        self.gun = Gun() 
        self.x = x
        self.y = y
        self.angle = angle
        self.r = 50

    def draw(self, canvas):
        #creates a triangle pointing in the direction of the mouse
        angle = self.angle
        canvas.create_polygon((self.x + self.r*math.cos(angle+math.pi/36), self.y + self.r*math.sin(angle+math.pi/36)),
                             (self.x + self.r*math.cos(angle-math.pi/36), self.y + self.r*math.sin(angle-math.pi/36)),
                             (self.x + (self.r+20)*math.cos(angle), self.y + (self.r+20)*math.sin(angle)))
        img = PhotoImage(file="Images/player.gif")      
        canvas.create_image(self.x-self.r,self.y-self.r, anchor=NW, image=img) 