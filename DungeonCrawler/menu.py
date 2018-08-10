from tkinter import *
import game
import levelEditor
from player import *

#taken from course website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def init(data):
    data.instructions = False
    data.levelSelect = False

def mousePressed(event, data):
    if data.levelSelect:
        count = 0
        for y in range(250, 650, 50):
            if count >= len(data.levels): return
            if y<event.y<y+50:
                data.mode = "game"
                data.room = data.levels[count]
                data.player = Player(data.width//2, data.height-100)
                game.init(data)
            count += 1
        return
    if (data.width//4<event.x<data.width*3//4 and
        data.height//3<event.y<data.height*4//9):
        data.mode = "game"
        game.newGame(data)
    elif (data.width//4<event.x<data.width*3//4 and 
        data.height*4/9<event.y<data.height*3/5):
        data.levelSelect = True
    elif (data.width//4<event.x<data.width*3//4 and 
        data.height*3/5<event.y<data.height*5/7):
        data.mode = "level editor" 
        levelEditor.init(data)
    elif (data.width//4<event.x<data.width*3//4 and 
        data.height*5/7<event.y<data.height*8/9):
        data.instructions = True

def keyPressed(event, data):
    if data.instructions or data.levelSelect:
        if event.keysym == "Escape":
            data.instructions = False
            data.levelSelect = False

def redrawAll(canvas, data):
    canvas.create_text(data.width//2, data.height//5, text = "DUNGEON CRAWLER", 
                       font = "Castellar 60 bold", fill = "white")
    canvas.create_text(data.width//2, data.height*3//5, text = "New Game\n\nLoad Custom Level\n\nLevel Editor\n\nInstructions", 
                       font = "Castellar 30", fill = "yellow", justify = "center")
    if data.levelSelect:
        content = readFile("customLevels.txt")
        levels = []
        for line in content.splitlines():
            levels.append(line.split(':')[0])
        margin = 100
        canvas.create_rectangle(margin, margin, data.width-margin, data.height, fill = "black")
        canvas.create_text(data.width//2, margin + 100, text = "Choose Level:",
                          font = "Arial 20", fill = "white")
        for index in range(len(levels)):
            canvas.create_text(data.width//2, margin+150+50*index,  text = levels[index],
                          font = "Arial 15", fill = "white")
        data.levels = levels
    elif data.instructions:
        margin = 150
        msg = "Press 'esc' to pause game\nUse the arrow keys to move\nPoint and click to shoot"
        canvas.create_rectangle(margin, margin, data.width-margin, data.height-margin, fill = "black")
        canvas.create_text(data.width//2, data.height//2, text = msg, font = "Arial 20", fill = "white")
        canvas.create_text(data.width//2, data.height*5//7, 
                           text = "Press 'esc' to go back to menu", font = "Arial 15", fill = "white")