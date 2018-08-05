from tkinter import *
from player import *
from enemy import *
import room1
import room2
import guns
import math

def init(data):
    data.player = Player("Killian", data.width//2, data.height//2, math.pi)
    data.myBullets = []
    data.enemyBullets = []
    data.up = False
    data.down = False
    data.left = False
    data.right = False
    data.shooting = False
    data.dead = False
    data.heart = PhotoImage(file="Images/heart.gif")
    data.emptyHeart = PhotoImage(file="Images/emptyHeart.gif")
    data.coin = PhotoImage(file = "Images/coin.gif")

def mousePressed(event, data):
    if data.dead: return
    r = data.player.r
    if data.player.gun == "pistol":
        data.myBullets.append(guns.shoot(data.player.x+r*math.cos(data.player.angle), 
                                         data.player.y+r*math.sin(data.player.angle), 
                                         data.player.angle))

def keyPressed(event, data):
    if data.dead: return
    if event.keysym == "Up" and not data.up:
        data.up = True
    elif event.keysym == "Down" and not data.down:
        data.down = True
    elif event.keysym == "Right" and not data.right:
        data.right = True
    elif event.keysym == "Left" and not data.left:
        data.left = True

def keyReleased(event, data):
    if data.dead: return
    if event.keysym == "Up" and data.up:
        data.up = False
    elif event.keysym == "Down" and data.down:
        data.down = False
    elif event.keysym == "Right" and data.right:
        data.right = False
    elif event.keysym == "Left" and data.left:
        data.left = False

def timerFired(data):
    if data.dead: return
    data.player.move(data)
    for bullet in data.myBullets:
        bullet.move()
        if bullet.collisionWithWall(data) or bullet.collisionWithBullet(data):
            data.myBullets.remove(bullet)
        elif bullet.collisionWithEnemy(data):
            data.myBullets.remove(bullet)
    for bullet in data.enemyBullets:
        bullet.move()
        if bullet.collisionWithMe(data.player):
            data.player.currHealth -= 1
            data.enemyBullets = []
            if data.player.currHealth <= 0:
                data.dead = True
            return
            data.enemyBullets.remove(bullet)
        if bullet.collisionWithWall(data):
            data.enemyBullets.remove(bullet)

    for enemy in data.enemies:
        if enemy.health <= 0:
            data.enemies.remove(enemy)
            data.player.gold += 5
            if isinstance(enemy, BigEnemy1): data.player.gold += 5
        enemy.onTimerFired(data)

def motion(event, data):
    if data.dead: return
    data.player.changeAngle(event, data)
        

def redrawAll(canvas, data):
    #should make hearts to show life
    iconSize = 50
    for i in range(data.player.health):
        if i>=data.player.currHealth:
            canvas.create_image(i*iconSize, 0, anchor=NW, image=data.emptyHeart)
        else: 
            canvas.create_image(i*iconSize, 0, anchor=NW, image=data.heart)
    #coin counter
    canvas.create_image(0, iconSize, anchor = NW, image = data.coin)
    canvas.create_text(iconSize*2,iconSize*1.5, font = "Impact 20", text = str(data.player.gold))
    data.player.draw(canvas)
    for enemy in data.enemies:
        enemy.draw(canvas)
    for bullet in data.enemyBullets:
        bullet.draw(canvas)
    for bullet in data.myBullets:
        bullet.draw(canvas)
    if data.dead:
        canvas.create_rectangle(data.width//2-200, data.height//2-50,
                               data.width//2+200, data.height//2+50, fill = "black")
        canvas.create_text(data.width//2, data.height//2, text = "You Died",
                          font = "Impact 30", fill = "red")