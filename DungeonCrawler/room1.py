from enemy import *
from barrier import *

def init(data):
    data.enemies = [Enemy(data.width//4, data.height//2), Shotgun(data.width*4/5, 10), 
                    MachineGunEnemy(data.width*2/3, data.height*4/5)]
    data.barriers = [Barrier(data.width*5//8,data.height/2, data.width*5//8, data.height, data.width, data.height)]