from tkinter import *
from player import *
from enemy import *
from levels import *
import guns
import math
import menu

#taken from course website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#taken from course website
def writeFile (path, contents):
    with open (path, "wt") as f:
        f.write(contents)

def save(data):
    contents = str(data.room), data.player.gun, str(data.player.gold) + " "
    for index in range(len(guns)):
        contents +=guns[index]
        if index != len(guns)-1:
            contents += ","
    writeFile("save.txt", contents)

def init(data):
    data.myBullets = []
    data.enemyBullets = []
    data.up = False
    data.down = False
    data.left = False
    data.right = False
    data.shooting = False
    data.dead = False
    if data.room == 1: room1(data)
    elif data.room == 2: room2(data)

def newGame(data):
    data.room=1
    data.player = Player(data.width//2, data.height-100)
    init(data)

def load(data):
    try:
        rawContents = readFile("save.txt")
        contents = rawContents.split(" ")
        data.room = int(contents[0])
        gun = contents[1]
        gold = int(contents[2])
        guns = []
        for g in contents[3].split(","):
            guns.append(g)
        data.player = Player(data.width//2, data.height-100, gun, gold, guns)
        init(data)
    except: 
        newGame(data)

def mousePressed(event, data):
    if data.dead: return
    r = data.player.r
    if data.player.gun == "pistol":
        data.myBullets.append(guns.shoot(data.player.x+r*math.cos(data.player.angle), 
                                         data.player.y+r*math.sin(data.player.angle), 
                                         data.player.angle))

def keyPressed(event, data):
    if data.dead: 
        if event.keysym == "Escape": 
            data.mode = "menu"
            menu.init(data)
        return
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
        if not bullet.move(data): data.myBullets.remove(bullet)
        if bullet.collisionWithWall(data) or bullet.collisionWithBullet(data):
            data.myBullets.remove(bullet)
        elif bullet.collisionWithEnemy(data):
            data.myBullets.remove(bullet)
    for bullet in data.enemyBullets:
        if not bullet.move(data): data.enemyBullets.remove(bullet)
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
    data.player.draw(canvas)
    for enemy in data.enemies:
        enemy.draw(canvas)
    for bullet in data.enemyBullets:
        bullet.draw(canvas)
    for bullet in data.myBullets:
        bullet.draw(canvas)
    for b in data.barriers:
        b.draw(canvas)
    canvas.create_rectangle(-1,-1, 153, 100, fill = "white", width = 5)
    #should make hearts to show life
    iconSize = 50
    for i in range(data.player.health):
        if i>=data.player.currHealth:
            canvas.create_image(i*iconSize, 0, anchor=NW, image=data.emptyHeart)
        else: 
            canvas.create_image(i*iconSize, 0, anchor=NW, image=data.heart)
    #coin counter
    canvas.create_image(0, iconSize-3, anchor = NW, image = data.coin)
    canvas.create_text(iconSize*2,iconSize*1.5, font = "Impact 20", text = str(data.player.gold))
    if data.dead:
        canvas.create_rectangle(data.width//2-200, data.height//2-50,
                               data.width//2+200, data.height//2+100, fill = "black")
        canvas.create_text(data.width//2, data.height//2, text = "You Died",
                          font = "Castellar 30", fill = "red")
        canvas.create_text(data.width//2, data.height//2+50, text = "Press 'esc' to restart",
                          font = "Arial 20", fill = "white")