from player import *
from tkinter import *

def dist(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def init(data):
    data.player.changePosition(data.width-data.player.r, data.height//2)
    data.heartPos = (data.width//2, data.height//2)
    data.roomCleared = True
    data.endBehavior = ["","",1,""]
    data.barriers = []

def keyPressed(event, data):
    if event.keysym == "Up" and not data.up:
        data.up = True
    elif event.keysym == "Down" and not data.down:
        data.down = True
    elif event.keysym == "Right" and not data.right:
        data.right = True
    elif event.keysym == "Left" and not data.left:
        data.left = True
    elif event.keysym == "e": 
        if (data.player.currHealth != data.player.health and
            data.player.gold >= 10 and 
            dist(data.player.x, data.player.y, data.heartPos[0], data.heartPos[1]) <= 250):
            data.player.gold -= 10
            data.player.currHealth += 1
            

def keyReleased(event, data):
    if event.keysym == "Up" and data.up:
        data.up = False
    elif event.keysym == "Down" and data.down:
        data.down = False
    elif event.keysym == "Right" and data.right:
        data.right = False
    elif event.keysym == "Left" and data.left:
        data.left = False

def timerFired(data):
    data.player.move(data)

def redrawAll(canvas, data):
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
    canvas.create_image(data.heartPos[0]-25, data.heartPos[1]-22, anchor=NW, image=data.heart)
    data.player.draw(canvas)
    if dist(data.player.x, data.player.y, data.heartPos[0], data.heartPos[1]) <= 250:
        canvas.create_text(data.width//2, data.height//2-250, text = "Press E to trade 10 gold for 1 heart",
                          font = "Castellar 30", fill = "yellow")