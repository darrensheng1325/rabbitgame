from pgzhelper import Actor
from random import randint
from config import MAP_SIZE
trees = [Actor("tree") for i in range(150)]
treepos = []
for i in trees:
    i.x = randint(-MAP_SIZE, MAP_SIZE)
    i.y = randint(-MAP_SIZE, MAP_SIZE)
for i in trees:
    treepos.append([i.x, i.y])