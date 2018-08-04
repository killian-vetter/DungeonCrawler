class Gun(object):
    def __init__(self):
        pass

class Bullet(object):
    def __init__(self, x, y, angle, color, size, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.size = size
        self.speed = speed
    #def move()