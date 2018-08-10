from enemy import *
from barrier import *
from tkinter import simpledialog
from tkinter import messagebox
import menu

#taken from course website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#taken from course website
def writeFile (path, contents):
    with open (path, "wt") as f:
        f.write(contents)

def save(name, data):
    contents = readFile("customLevels.txt")
    level = name + ":"
    for enemy in data.enemies:
        level += str(enemy) +":"
    for barrier in data.barriers:
        level += str(barrier) + ":"
    if len(contents)<=1:
        writeFile ("customLevels.txt", level[:-1])
    else:
        writeFile ("customLevels.txt", contents + "\n" + level[:-1])

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

def keyPressed(event, data, canvas):
    if event.keysym == "Escape":
        data.pause = True
        data.selection = None
    elif data.pause:
        if event.keysym == "Escape":
            data.pause = False
        if event.keysym == "m":
            data.mode = "menu"
            menu.init(data)
        elif event.keysym == "s":
            name = simpledialog.askstring("Input", "Name of file (don't use ':'): ", 
                              parent=canvas)
            if ":" in name:
                messagebox.showerror("Error", "':' is not allowed in the level name")
            elif name is not None:
                save(name, data)
                messagebox.showinfo("Information","Saved!")

def b1Motion (event, data):
    if data.pause: return
    if isinstance(data.selection, Enemy):
        data.selection.x = event.x
        data.selection.y = event.y

def mousePressed(event, data, canvas):
    if data.pause: return
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
        elif isinstance(elem, Barrier) and elem.point1[0]-10<=event.x<=elem.point2[0]+10 and \
            elem.point1[1]-10<=event.y<=elem.point2[1]+10:
            answer = simpledialog.askinteger("Input", "What percent of the the screen should this be(interger 1-80)?", 
                              parent=canvas,
                               minvalue=1, maxvalue=80)
            if answer is not None:
                if elem.point1[0] == elem.point2[0]:
                    data.selection = Barrier(event.x, event.y, event.x, event.y-data.height*answer//100, data.width, data.height)
                else: 
                    data.selection = data.selection = Barrier(event.x, event.y, event.x-data.width*answer//100, event.y, data.width, data.height)


def mouseRelease(event, data):
    if data.pause: return
    if isinstance(data.selection, Enemy):
        data.enemies.append(data.selection)
        data.selection = None

def motion(event, data):
    if data.pause: return
    if isinstance(data.selection, Barrier):
        data.selection.shift(event.x, event.y)

def redrawAll(canvas, data):
    if isinstance(data.selection, Enemy):
        data.selection.draw(canvas)
    elif isinstance(data.selection, Barrier):
        data.selection.drawOther(canvas)

    for enemy in data.enemies:
        enemy.draw(canvas)

    for barrier in data.barriers:
        barrier.draw(canvas)

    canvas.create_rectangle(0, data.height*4//5, data.width, data.height, fill = "white")

    for elem in data.selectionMenu:
        if isinstance(elem, Barrier):
            elem.drawOther(canvas)
        else: 
            elem.draw(canvas)

    canvas.create_text(data.width//2, data.height*9//10, text = "Drage and drop enemies\nClick barrier, choose size, and drop", 
                       font = "Castellar 20", fill = "black", justify = "center")

    if data.pause:
        margin = 150
        msg = "Press 'S' to save"
        canvas.create_rectangle(margin, margin, data.width-margin, data.height-margin, fill = "black")
        canvas.create_text(data.width//2, data.height//2, text = msg, font = "Arial 20", fill = "white")
        canvas.create_text(data.width//2, data.height*5//7, 
                           text = "Press 'M' to go back to menu", font = "Arial 15", fill = "white")