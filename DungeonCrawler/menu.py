from tkinter import *
import game

def init(data):
    data.instructions = False

def mousePressed(event, data):
    if (data.width//4<event.x<data.width*3//4 and
        data.height//3<event.y<data.height*4//9):
        data.mode = "game"
        game.newGame(data)
    elif (data.width//4<event.x<data.width*3//4 and 
        data.height*4/9<event.y<data.height*3/5):
        data.mode = "game"
        game.load(data)
    elif (data.width//4<event.x<data.width*3//4 and 
        data.height*3/5<event.y<data.height*5/7):
        print ("level editor") #level editor function
    elif (data.width//4<event.x<data.width*3//4 and 
        data.height*5/7<event.y<data.height*8/9):
        print ("isntr")
        data.instructions = True

def keyPressed(event, data):
    if data.instructions:
        print ("maybe")
        if event.keysym == "Escape":
            print ("works")
            data.instructions = False

def redrawAll(canvas, data):
    canvas.create_text(data.width//2, data.height//5, text = "DUNGEON CRAWLER", 
                       font = "Castellar 60 bold", fill = "white")
    canvas.create_text(data.width//2, data.height*3//5, text = "New Game\n\nLoad Game\n\nLevel Editor\n\nInstructions", 
                       font = "Castellar 30", fill = "yellow", justify = "center")
    if data.instructions:
        margin = 100
        msg = "Press 'esc' to pause game\nUse the arrow keys to move\nPoint and click to shoot"
        canvas.create_rectangle(margin, margin, data.width-margin, data.height-margin, fill = "black")
        canvas.create_text(data.width//2, data.height*2//5, text = msg, font = "Arial 20", fill = "white")
        canvas.create_text(data.width//2, data.height*3//4, 
                           text = "Press 'esc' to go back to menu", font = "Arial 15", fill = "white")