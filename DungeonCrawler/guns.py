import math

def shoot(x, y, angle):
    return Bullet(x, y, 5, angle, "red", 20)

class Bullet(object):
    def __init__(self, x, y, r, angle, color, speed):
        self.x = x
        self.y = y
        self.r = r
        self.angle = angle
        self.color = color
        self.speed = speed

    def move(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)

    def draw(self, canvas):
        x, y, r = self.x, self.y, self.r
        canvas.create_oval(x-r,y-r,x+r,y+r, fill = self.color)