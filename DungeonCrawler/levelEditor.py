from enemy import *
from barrier import *

def init(data):
    data.barriers = []
    data.enemies = []
    data.paused = False
    data.selectionMenu = [Enemy(10,data.height*4//5+25), Shotgun(120,data.height*4//5+25), 
                          MachineGunEnemy(230, data.height*4//5+25), 
                          Barrier(data.width- 10, data.height*9//10, data.width - 210, data.height*9//10, data.width, data.height), 
                          Barrier(data.width - 250, data.height-10, data.width - 250, data.height*4//5+10, data.width, data.height)]
    data.selection = None
    data.pause = False

def keyPressed(event, data):
    if event.keysym == "Escape":
        data.pause = True
        data.selection = None

def b1Motion (event, data):
    if isinstance(data.selection, Enemy):
        data.selection.x = event.x
        data.selection.y = event.y

def mousePressed(event, data):
    if isinstance(data.selection, Barrier):
        data.barriers.append(data.selection)
        data.selection = None
    for elem in data.selectionMenu:
        if isinstance(elem, Enemy) and elem.x<=event.x<=elem.w+elem.x and \
            elem.y <= event.y <= elem.h + elem.y:
            if isinstance (elem, MachineGunEnemy):
                data.selection = MachineGunEnemy(event.x, event.y)
            elif isinstance(elem, Shotgun):
                data.selection = Shotgun(event.x, event.y)
            else:
                data.selection = Enemy(event.x, event.y)
        else:
            pass #write stuff for barriers later

def mouseRelease(event, data):
    if isinstance(data.selection, Enemy):
        data.enemies.append(data.selection)
        data.selection = None

def motion(event, data):
    if isinstance(data.selection, Barrier):
        data.selection.shift(event.x, event.y)

def redrawAll(canvas, data):
    canvas.create_rectangle(0, data.height*4//5, data.width, data.height, fill = "white")

    for elem in data.selectionMenu:
        if isinstance(elem, Barrier):
            elem.drawOther(canvas)
        else: 
            elem.draw(canvas)

    if isinstance(data.selection, Enemy):
        data.selection.draw(canvas)
    elif isinstance(data.selection, Barrier):
        data.selection.drawOther(canvas)

    for enemy in data.enemies:
        enemy.draw(canvas)

    for barrier in data.barriers:
        barrier.draw(canvas)

    canvas.create_text(data.width//2, data.height*9//10, text = "Drage and drop enemies\nClick barrier, choose size, and drop", 
                       font = "Castellar 20", fill = "black", justify = "center")