# Basic Animation Framework

from tkinter import *
from player import *
import math

####################################
# customize these functions
####################################

def init(data):
    data.player = Player("Killian", data.width//2, data.height//2, math.pi)
    data.up = False
    data.down = False
    data.left = False
    data.right = False
    data.shooting = False
    data.dead = False

def mousePressed(event, data):
    if data.dead: return

def keyPressed(event, data):
    if data.dead: return
    if event.keysym == "Up":
        data.up = True
    elif event.keysym == "Down":
        data.down = True
    elif event.keysym == "Right":
        data.right = True
    elif event.keysym == "Left":
        data.left = True

def keyReleased(event, data):
    if data.dead: return
    if event.keysym == "Up":
        data.up = False
    elif event.keysym == "Down":
        data.down = False
    elif event.keysym == "Right":
        data.right = False
    elif event.keysym == "Left":
        data.left = False

def timerFired(data):
    pass

def motion(event, data):
    data.player.changeAngle(event, data)
        

def redrawAll(canvas, data):
    data.player.draw(canvas)

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
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1280, 680)
