from tkinter import *
import game

def mousePressed(event, data):
    if (data.width//4<event.x<data.width*3//4 and
        data.height//3<event.y<data.height//2):
        data.mode = "game"
        game.init(data)

def redrawAll(canvas, data):
    canvas.create_text(data.width//2, data.height//5, text = "DUNGEON CRAWLER", 
                       font = "Castellar 60 bold", fill = "white")
    canvas.create_text(data.width//2, data.height*3//5, text = "New Game\n\nLoad Game\n\nLevel Editor", 
                       font = "Castellar 40", fill = "yellow", justify = "center")