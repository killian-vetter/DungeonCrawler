from guns import *
from tkinter import *
import math

#taken from course website: http://www.cs.cmu.edu/~112n18/
def roundHalfUp(num):
    if num%1>=.5: num += 1
    return int(num)

#player initially has 3 health 
class Player (object):
    def __init__(self, x, y, gun = "pistol", gold = 0, guns = ["pistol"]):
        self.health = 3
        self.currHealth = self.health
        self.guns = guns
        self.gun = gun
        self.x = x
        self.y = y
        self.angle = 0
        self.gold = gold
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

    def move(self, data):
        dir = [0,0]
        if data.up:
            dir[1] -= 10
        if data.down: 
            dir[1] += 10
        if data.left:
            dir[0] -= 10
        if data.right:
            dir[0] += 10
        #self.checkBarrierCollision(dir, data)
        self.x += dir[0]
        self.y += dir[1]
        if self.x<self.r: self.x=self.r
        elif self.x>data.width-self.r: self.x = data.width-self.r
        if self.y<self.r: self.y=self.r
        elif self.y>data.height-self.r: self.y = data.height-self.r

    def checkBarrierCollision(self, dir, data):
        if dir[0] == 0 and dir[1] == 0: return False
        if dir[0] == 0: #less strict
            sign = roundHalfUp(dir[1]/abs(dir[1]))
            for change in range(0, dir[1], sign):
                for barrier in data.barriers:
                    if self.y+change+self.r<=barrier.point1[1] and (self.x+self.r<barrier.point1[0] or self.x-self.r>barrier.point2[0]):
                        self.y = self.y+change
                        dir[1] = 0
                        return True
                    elif self.y+change-self.r>=barrier.point2[1] and (self.x+self.r<barrier.point1[0] or self.x-self.r>barrier.point2[0]):
                        self.y = self.y+change
                        dir[1] = 0
                        return True
        elif dir[1] == 0: #more strict
            sign = roundHalfUp(dir[0]/abs(dir[0]))
            for change in range(0, dir[0], sign):
                for barrier in data.barriers:
                    if self.x+change+self.r<=barrier.point1[0] and (self.y+self.r<barrier.point1[1] or self.y-self.r>barrier.point2[1]):
                        self.x = self.x+change
                        dir[0] = 0
                        return True
                    elif self.x+change-self.r>=barrier.point2[0] and (self.y+self.r<barrier.point1[1] or self.y-self.r>barrier.point2[1]):
                        self.x = self.x+change
                        dir[0] = 0
                        return True
        else: #less strict
            xsign = roundHalfUp(dir[0]/abs(dir[0]))
            ysign = roundHalfUp(dir[1]/abs(dir[1]) * xsign)
            boolean = False
            for change in range(0, dir[0], xsign):
                for barrier in data.barriers:
                    if self.x+change+self.r>=barrier.point1[0] and (self.y+self.r<barrier.point1[1] or self.y-self.r>barrier.point2[1]):
                        self.x = self.x+change
                        self.y = self.y+change*ysign
                        dir[1] -= change*ysign
                        dir[0] = 0
                        boolean = True
                    elif self.x+change-self.r<=barrier.point2[0] and (self.y+self.r<barrier.point1[1] or self.y-self.r>barrier.point2[1]):
                        self.x = self.x+change
                        self.y = self.y+change*ysign
                        dir[1] -= change*ysign
                        dir[0] = 0
                        boolean = True
                    if self.y+change*ysign+self.r<=barrier.point1[1] and (self.x+self.r<barrier.point1[0] or self.x-self.r>barrier.point2[0]):
                        self.y = self.y+change*ysign
                        dir[1] = 0
                        dir[0] -= change
                        boolean = True
                    elif self.y+change*ysign-self.r>=barrier.point2[1] and (self.x+self.r<barrier.point1[0] or self.x-self.r>barrier.point2[0]):
                        self.y = self.y+change*ysign
                        dir[1] = 0
                        dir[0] -= change
                        boolean = True
                if boolean: return True
        return False

    def changeLocation(self, x, y):
        self.x = x
        self.y = y

    #the polygon makes a triangle point at cursor
    def draw(self, canvas):
        #creates a triangle pointing in the direction of the mouse
        angle = self.angle
        canvas.create_image(self.x-self.r, self.y-self.r, anchor=NW, image=self.img)
        canvas.create_polygon((self.x + self.r*math.cos(angle+math.pi/30), self.y + self.r*math.sin(angle+math.pi/30)),
                             (self.x + self.r*math.cos(angle-math.pi/30), self.y + self.r*math.sin(angle-math.pi/30)),
                             (self.x + (self.r+20)*math.cos(angle), self.y + (self.r+20)*math.sin(angle)))