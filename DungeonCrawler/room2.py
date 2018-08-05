from enemy import *

def init(data):
    data.enemies = [BigEnemy1(data.width//4, data.height//2)]
    data.barriers = []