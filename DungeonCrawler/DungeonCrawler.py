# Basic Animation Framework

from tkinter import *
from player import *
import math

####################################
# Helper Functions
####################################

def movePlayer(data):
    dir = [0,0]
    if data.up:
        dir[1] -= 5
    if data.down: 
        dir[1] += 5
    if data.left:
        dir[0] -= 5
    if data.right:
        dir[0] += 5
    data.player.move(dir, data)

####################################
# Binded Functions
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
    #print (data.keysym)
    if event.keysym == "Up" and data.up:
        data.up = False
    elif event.keysym == "Down" and data.down:
        data.down = False
    elif event.keysym == "Right" and data.right:
        data.right = False
    elif event.keysym == "Left" and data.left:
        data.left = False

def timerFired(data):
    movePlayer(data)

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
    root.bind("<KeyRelease>", lambda event:
                            keyReleasedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1280, 680)
