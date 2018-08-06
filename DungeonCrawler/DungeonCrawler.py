'''
Cite Images
Coin: https://www.pixilart.com/art/coin-gif-7736b1d30d303e4
Heart: https://gifer.com/en/DDt
Cobblestone floor: http://www.dundjinni.com/forums/forum_posts.asp?TID=13815&KW=tile+set
Swordman: https://www.reddit.com/r/PixelArt/comments/4706xm/occcnew_to_pixel_art_first_attempt_at_animation/
Goomba: https://society6.com/product/pixel-goomba-super-mario-bros_print

 Basic Animation Framework from course website: http://www.cs.cmu.edu/~112n18/notes/notes-animations-part1.html
 '''

from tkinter import *
from player import *
from enemy import *
import room1
import room2
import basicActions
import guns
import math

####################################
# Binded Functions
####################################

#modes are "menu", "game", "level editor"
def init(data):
    data.test = PhotoImage(file = "Images/test.gif")
    data.floor = PhotoImage(file = "Images/floor.gif")
    data.heart = PhotoImage(file="Images/heart.gif")
    data.emptyHeart = PhotoImage(file="Images/emptyHeart.gif")
    data.coin = PhotoImage(file = "Images/coin.gif")
    data.mode = "menu"
    basicActions.init(data)
    room1.init(data)

def mousePressed(event, data):
    basicActions.mousePressed(event, data)

def keyPressed(event, data):
    basicActions.keyPressed(event, data)

def keyReleased(event, data):
    basicActions.keyReleased(event, data)

def timerFired(data):
    basicActions.timerFired(data)

def motion(event, data):
    basicActions.motion(event, data)
        

def redrawAll(canvas, data):
    canvas.create_image(0, 0, anchor=NW, image=data.floor)
    basicActions.redrawAll(canvas, data)

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