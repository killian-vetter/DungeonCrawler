from enemy import *
from barrier import *

def init(data):
    #data.enemies = [Enemy(data.width//4, data.height//2), Shotgun(data.width*4/5, 10), 
    #                MachineGunEnemy(data.width*2/3, data.height*4/5)]
    data.enemies = []
    data.barriers = [Barrier(data.width*3/4,data.height/2, data.width*3/4, data.height-20, data.width, data.height)]