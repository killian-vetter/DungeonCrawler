from guns import *
from tkinter import *
import random
import math

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

#taken from course website
def almostEquals(d1, d2):
    epsilon = 10**-10
    return (abs(d2 - d1) < epsilon)

#The 2 functions below are taken from https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect 
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    #wrote this part myself to deal with colinearity- Killian
    x1 = A[0]-B[0]
    y1 = A[1]-B[1]
    x2 = C[0]-D[0]
    y2 = C[1]-D[1]
    if (x1 == 0 and x2 == 0 and A[0] == C[0]):
        return (A[1]<=C[1]<=B[1] or A[1]<=D[1]<=B[1])
    if not (x1 == 0 or x2 == 0):
        m1 = y1/x1
        m2 = y2/x2
        b1 = -A[0]*m1+A[1]
        b2 = -C[0]*m2+C[1]
        if (almostEquals(m1, m2) and almostEquals(b1, b2) and
             (A[0]<=C[0]<=B[0] or A[0]<=D[0]<=B[0])):
            return True
    #end of stuff written by me
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

#gets angle from the x y coordinates to a the tuple pos
def getAngle(x, y, pos):
    x = x - pos[0]
    y = y - pos[1]
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
        self.health = 5
        self.h = 100
        self.w = 100
        self.img = PhotoImage(file="Images/enemy.gif")
        self.angle = 0
        self.lifeTime = random.randint(0,50)

    #returns true if it is in the line of sight of the enemy
    def lineOfSightWithLine(self, pos, line):
        test1 = intersect((self.x, self.y), (pos[0], pos[1]), (line[0][0], line[0][1]), (line[1][0], line[1][1]))
        test2 = intersect((self.x+self.w//2, self.y), (pos[0], pos[1]), (line[0][0], line[0][1]), (line[1][0], line[1][1]))
        test3 = intersect((self.x-self.w//2, self.y), (pos[0], pos[1]), (line[0][0], line[0][1]), (line[1][0], line[1][1]))
        test4 = intersect((self.x, self.y+self.h//2), (pos[0], pos[1]), (line[0][0], line[0][1]), (line[1][0], line[1][1]))
        test5 = intersect((self.x, self.y-self.h//2), (pos[0], pos[1]), (line[0][0], line[0][1]), (line[1][0], line[1][1]))
        return not (test1 or test2 or test3 or test4 or test5)

    def lineOfSight(self, pos, barriers):
        for barrier in barriers:
            if not self.lineOfSightWithLine(pos,(barrier.point1, barrier.point2)):
                return False
        return True

    def move(self, data):
        line = [(self.x+self.w//2, self.y+self.h//2), (data.player.x, data.player.y)]
        target = (data.player.x, data.player.y)
        minN = -1
        for barrier in data.barriers:
            if not self.lineOfSightWithLine((data.player.x, data.player.y),(barrier.point1, barrier.point2)):
                for node in barrier.nodes:
                    temp = dist (self.x, self.y, node[0], node[1])
                    if temp > minN:
                        minN = temp
                        target = node
        self.angle = getAngle(self.x+self.w//2, self.y+self.h//2, target)
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)

    def shoot(self, data):
        data.enemyBullets.append(Bullet(self.x+self.w//2, self.y+self.h//2, 15, self.angle, "red", 10))

    #sets the angle to point at player. Moves toward player.
    #Shoots at player every 2 seconds
    def onTimerFired(self, data):
        self.move(data)
        self.lifeTime += 1
        if self.lifeTime % 20 == 0 and self.lineOfSight((data.player.x, data.player.y), data.barriers):
            self.shoot(data)
   
    def draw(self, canvas):
        canvas.create_image(self.x, self.y, anchor=NW, image=self.img)

class MachineGunEnemy (Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = PhotoImage(file="Images/machineGun.gif")

    def onTimerFired(self, data):
        self.move(data)
        self.lifeTime += 1
        if self.lifeTime % 8 == 0 and self.lineOfSight((data.player.x, data.player.y), data.barriers):
            data.enemyBullets.append(Bullet(self.x+self.w//2, self.y+self.h//2, 10, self.angle, "purple", 15))

class Shotgun (Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = PhotoImage(file="Images/shotgun.gif")

    def shoot(self, data):
        data.enemyBullets.append(Bullet(self.x+self.w//2, self.y+self.h//2,
                                       18, self.angle, "green", 10))
        data.enemyBullets.append(Bullet(self.x+self.w//2, self.y+self.h//2,
                                       18, self.angle+math.pi/18, "green", 10))
        data.enemyBullets.append(Bullet(self.x+self.w//2, self.y+self.h//2, 18,
                                       self.angle-math.pi/18, "green", 10))


class Boss (Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.health = 20
        self.h = 210
        self.w = 145
        #the hitbox varible records where the hitbox starts from h and w is the hitbox's size
        self.hitbox = [(0,75), (130, 90), (135, 0), (0,0)]
        #for each hitbox I do (width of image - widths of hitbox - x of hitbox, y of hitbox)
        self.hitboxR = [(150-self.w-self.hitbox[0][0], self.hitbox[0][1]),
                        (325-self.w-self.hitbox[1][0], self.hitbox[1][1]),
                        (290-self.w-self.hitbox[2][0], self.hitbox[2][1]),
                        (167-self.w-self.hitbox[3][0], self.hitbox[3][1])]
        self.imgs = [PhotoImage(file="Images/swordman1.gif"), PhotoImage(file="Images/swordman2.gif"),
                     PhotoImage(file="Images/swordman3.gif"), PhotoImage(file="Images/swordman4.gif")]
        self.imgsR = [PhotoImage(file="Images/swordman1R.gif"), PhotoImage(file="Images/swordman2R.gif"),
                     PhotoImage(file="Images/swordman3R.gif"), PhotoImage(file="Images/swordman4R.gif")]
        self.angle = 0
        self.lifeTime = random.randint(4,19)
        self.animation = 0

    def move(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)

    def shoot(self, data):
        if -math.pi/2 <= self.angle <= math.pi/2:
            x = self.x + self.w
        else:
            x = self.x
        y = self.y + self.h//3
        angleIncrement = math.pi/18
        for i in range(5):
            data.enemyBullets.append(Bullet(x, y, 15, self.angle+angleIncrement*i, "orange", 10))
            data.enemyBullets.append(Bullet(x, y, 15, self.angle-angleIncrement*i, "orange", 10))

    def onTimerFired(self, data):
        self.angle = getAngle(self.x, self.y, (data.player.x, data.player.y))
        self.move()
        if self.lifeTime % 20==1:
            self.animation = 1
        elif self.lifeTime % 20 == 2:
            self.animation = 2
            self.shoot(data)
        elif 3<=self.lifeTime %  20<=10:
            self.animation = 3
        else:
            self.animation = 0
        self.lifeTime += 1

    def draw(self, canvas):
        if -math.pi/2 <= self.angle <= math.pi/2:
            canvas.create_image(self.x-self.hitboxR[self.animation][0], self.y-self.hitboxR[self.animation][1], 
                             anchor=NW, image=self.imgsR[self.animation])
        else:
            canvas.create_image(self.x-self.hitbox[self.animation][0], self.y-self.hitbox[self.animation][1], 
                             anchor=NW, image=self.imgs[self.animation])