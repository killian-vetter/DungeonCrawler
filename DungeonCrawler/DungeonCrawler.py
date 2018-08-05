# Basic Animation Framework

from tkinter import *
from player import *
from enemy import *
import guns
import math

####################################
# Binded Functions
####################################

def init(data):
    data.player = Player("Killian", data.width//2, data.height//2, math.pi)
    data.myBullets = []
    data.enemyBullets = []
    data.enemies = [Enemy(data.width//4, data.height//2)]
    data.up = False
    data.down = False
    data.left = False
    data.right = False
    data.shooting = False
    data.dead = False
    data.heart = PhotoImage(file="Images/heart.gif")
    data.emptyHeart = PhotoImage(file="Images/emptyHeart.gif")

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
    for bullet in data.enemyBullets:
        bullet.move()
        if bullet.collisionWithMe(data.player):
            data.player.currHealth -= bullet.dmg
            data.enemyBullets = []
            if data.player.currHealth <= 0:
                data.dead = True
            return
            data.enemyBullets.remove(bullet)
        if bullet.collisionWithWall(data):
            data.enemyBullets.remove(bullet)

    for enemy in data.enemies:
        enemy.onTimerFired(data)

def motion(event, data):
    if data.dead: return
    data.player.changeAngle(event, data)
        

def redrawAll(canvas, data):
    #should make hearts to show life
    heartSize = 50
    for i in range(data.player.health):
        if i>=data.player.currHealth:
            canvas.create_image(i*heartSize, 0, anchor=NW, image=data.emptyHeart)
        else: 
            canvas.create_image(i*heartSize, 0, anchor=NW, image=data.heart)
    data.player.draw(canvas)
    for bullet in data.myBullets:
        bullet.draw(canvas)
    for bullet in data.enemyBullets:
        bullet.draw(canvas)
    for enemy in data.enemies:
        enemy.draw(canvas)
    if data.dead:
        canvas.create_rectangle(data.width//2-200, data.height//2-50,
                               data.width//2+200, data.height//2+50, fill = "black")
        canvas.create_text(data.width//2, data.height//2, text = "You Died",
                          font = "Impact 30", fill = "red")

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyReleasedWrapper(event, canvas, data):
        keyReleased(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    def motionWrapper(event):
        motion(event, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind('<Motion>', motionWrapper)
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<KeyRelease>", lambda event:
                            keyReleasedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1280, 680)