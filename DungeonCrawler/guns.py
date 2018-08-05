import math

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

#this is the shoot function of the basic pistol
def shoot(x, y, angle):
    return Bullet(x, y, 5, angle, "blue", 30)

class Bullet(object):
    def __init__(self, x, y, r, angle, color, speed):
        self.x = x
        self.y = y
        self.r = r
        self.angle = angle
        self.color = color
        self.speed = speed

    def collisionWithWall(self, data):
        return ((not data.width-self.r>self.x>self.r) or 
                (not data.height-self.r>self.y>self.r))

    def collisionWithBullet(self, data): 
        for bullet in data.enemyBullets:
            if dist(bullet.x, bullet.y, self.x, self.y)<=self.r+bullet.r:
                data.enemyBullets.remove(bullet)
                return True
        return False

    def collisionWithEnemy(self, data):
         for enemy in data.enemies:
             if enemy.w != -1 and enemy.h != -1:
                if ((enemy.x<=self.x-self.r<=enemy.x+enemy.w and enemy.y<=self.y-self.r<=enemy.y+enemy.h) 
                    or (enemy.x<=self.x+self.r<=enemy.x+enemy.w and enemy.y<=self.y-self.r<=enemy.y+enemy.h)
                    or (enemy.x<=self.x-self.r<=enemy.x+enemy.w and enemy.y<=self.y+self.r<=enemy.y+enemy.h)
                    or (enemy.x<=self.x+self.r<=enemy.x+enemy.w and enemy.y<=self.y+self.r<=enemy.y+enemy.h)):
                    enemy.health -= 1
                    return True
             elif dist(enemy.x+enemy.r, enemy.y+enemy.r, self.x , self.y) <= enemy.r + self.r:
                 enemy.health -= 1
                 return True
         return False

    def collisionWithMe(self, player):
        return dist(self.x, self.y, player.x, player.y) <= self.r + player.r

    def move(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)

    def draw(self, canvas):
        x, y, r = self.x, self.y, self.r
        canvas.create_oval(x-r,y-r,x+r,y+r, fill = self.color)