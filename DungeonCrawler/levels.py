from enemy import *
from barrier import *
from player import *

#taken from course website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#end behavior goes left, up, right, up
def room1(data):
    data.roomCleared = False
    data.enemies = [Enemy(data.width*3//4, 120), Shotgun(data.width*4/5, 10), 
                    MachineGunEnemy(data.width*2/3, data.height*4/5)]
    data.barriers = [Barrier(data.width//2, 0, data.width//2, data.height*3//5, data.width, data.height)]
    data.myBullets = []
    data.enemyBullets = []
    data.endBehavior = ["Store", 2, "", ""]
    data.player.changePosition(data.width//2, data.height-100)

def room2(data):
    data.roomCleared = False
    data.enemies = [Shotgun(data.width//5, data.height//5), Shotgun(data.width*4//5, data.height//5),
                    MachineGunEnemy(data.width*4//5, data.height*4//5)]
    data.barriers = [Barrier(data.width//3, data.height//3, data.width//3, data.height, data.width, data.height), 
                     Barrier(data.width*2//3, data.height, data.width*2//3, data.height*2//3, data.width, data.height)]
    data.myBullets = []
    data.enemyBullets = []
    data.endBehavior = ["", 3, "", 1]
    data.player.changePosition(data.width//2, data.height-100)

def room3(data):
    data.endBehavior = ["", "", "", ""]
    data.enemies = [Boss(data.width//4, data.height//3)]
    data.barriers = []
    data.myBullets = []
    data.enemyBullets = []
    data.roomCleared = False
    data.player.changePosition(data.width//2, data.height-100)

def customRoom(data):
    data.enemies = []
    data.barriers = []
    contents = readFile("customLevels.txt")
    for line in contents.splitlines():
        line = line.split(":")
        for index in range(len(line)):
            if index == 0 and line[index] != data.room:
                break
            if index != 0:
                elem = line[index].split(" ")
                if elem[0] == "Enemy":
                    data.enemies.append(Enemy(int(elem[1]),int(elem[2])))
                elif elem[0] == "Shotgun":
                    data.enemies.append(Shotgun(int(elem[1]),int(elem[2])))
                elif elem[0] == "MachineGunEnemy":
                    data.enemies.append(MachineGunEnemy(int(elem[1]),int(elem[2])))
                elif elem[0] == "Barrier":
                    data.barriers.append(Barrier(int(elem[1]), int(elem[2]), int(elem[3]), int(elem[4]), data.width, data.height))
    data.myBullets = []
    data.enemyBullets = []
    data.roomCleared = False
    data.player.changePosition(data.width//2, data.height-100)
    data.endBehavior = ["", "", "", ""]