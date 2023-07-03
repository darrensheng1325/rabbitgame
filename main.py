from pgzrun import *
from random import *
from time import sleep
from threading import Thread
HEIGHT = 750
WIDTH = HEIGHT
MAP_SIZE = 2700
cursor = Actor("cursor")
inventoryactor = Actor("inventory")
cat = Actor("cat")
hud = Actor("hud")
trees = [Actor("tree") for i in range(150)]
treepos = []
rabbit = Actor("rabbit")
rabbitpos = [{"x":randint(-MAP_SIZE, MAP_SIZE),"y":randint(-MAP_SIZE, MAP_SIZE), "has_rabbit":True} for i in range(25)]
# rabbitpos = [
#     [0, 0],
#     [90, 90],
#     #[-90, 0],
#     #[-90, 90],
# ]\
saved_rabbit_pos = [0, 0]
for i in trees:
    i.x = randint(-MAP_SIZE, MAP_SIZE)
    i.y = randint(-MAP_SIZE, MAP_SIZE)
for i in trees:
    treepos.append([i.x, i.y])
water = Actor("water")
cat.y = HEIGHT/2
cat.x = WIDTH/2
camerascrolly = 0
camerascrollx = 0
counter = 0
rabbit_dead = False
rabbit_health = 10
rabbit.pos = (10000, 10000)
rabbit_model_pos = [0, 0]
cat_model_pos = [0, 0]
game_clock = Actor("clock")
game_clock.x = 25
game_clock.y = 25
day_in_millis = 100
timer = 2
night_overlay = Actor("night_overlay")
background_color = (0, 255, 255)
night_color = (0, 0, 0)
screen_background_color = (0, 255, 255)
apples = [Actor("apple") for i in range(len(trees)//2)]
apples_model_pos = [[100000, 100000] for i in range(len(apples))]
apples_collected = [False for i in range(len(apples))]
inventoryslots = []
for i in range(25):
    inventoryslots.append([30*i+15, 700])
for index, i in enumerate(apples):
    if randint(0, 1) == 1:
        apples_model_pos[index] = treepos[index]
        
class Inventory:
    def __init__ (self, slots, entity):
        self.slots = slots
        self.entity = entity
        self.item_num = 0
        self.items = []
    def drop(self, item, index):
        self.item_num -= 1
    def append(self, item, index):
        try:
            item.x = self.slots[self.item_num][0]
            item.y = self.slots[self.item_num][1]
            self.items.append(item)
            self.item_num += 1
        except Exception:
            self.drop(item, index)

def draw():
    screen.fill(screen_background_color)
    water.draw()
    cat.draw()
    for i in trees:
        i.draw()
    rabbit.x = rabbit_model_pos[0] + camerascrollx
    rabbit.y = rabbit_model_pos[1] + camerascrolly
    
    if rabbit.colliderect(hud):
        rabbit.draw()
    game_clock.draw()
    hud.draw()
    for index, i in enumerate(apples):
        if not apples_collected[index]:
            i.x = apples_model_pos[index][0] + camerascrollx
            i.y = apples_model_pos[index][1] + camerascrolly
    for i in apples:
        i.draw()
    for i in inventory.items:
        i.draw()

def update():
    global camerascrollx
    global camerascrolly
    global counter
    global saved_rabbit_pos
    global rabbit_dead
    global rabbit_health
    for index, i in enumerate(trees):
        i.x = treepos[index][0] + camerascrollx
        i.y = treepos[index][1] + camerascrolly
    
    water.x = camerascrollx
    water.y = camerascrolly
    game_clock.angle = timer / day_in_millis + 180
    
    
def on_key_down(key):
    global camerascrollx
    global camerascrolly
    global apples
    global apples_collected
    if key == keys.UP:
        camerascrolly += 90
    if key == keys.DOWN:
        camerascrolly -= 90
    if key == keys.LEFT:
        camerascrollx += 90
    if key == keys.RIGHT:
        camerascrollx -= 90
    if key == keys.P:
        apples_data = pick_up_item(apples, cat, apples_collected)
        apples = apples_data[0]
        apples_collected = apples_data[1]
        

def update_rabbit():
    global saved_rabbit_pos
    global rabbit_dead
    global rabbit_health
    global counter
    global rabbit_model_pos
    global rabbitpos
    while True:
        counter += 1
#         cursor.x = rabbit.x + camerascrollx
#         cursor.y = rabbit.y + camerascrolly
        rabbit_dead = False
        if counter == len(rabbitpos):
            counter = 0

        sleep(1/120)
        rabbit_here = [rabbitpos[counter]["has_rabbit"]]
        if not hud.colliderect(rabbit):
            rabbit_model_pos = [rabbitpos[counter]["x"], rabbitpos[counter]["y"]]
            saved_rabbit_pos = rabbit_model_pos
            continue
        if not rabbit_here:
            continue
        
        rabbit_model_pos = saved_rabbit_pos
        while not rabbit_dead:
            cat_model_pos = [cat.x - camerascrollx, cat.y - camerascrolly]
            # rabbit.pos = (saved_rabbit_pos[0], saved_rabbit_pos[1])
            if rabbit_model_pos[1] > cat_model_pos[1]:
                rabbit_model_pos[1] -= 3
            if rabbit_model_pos[1] < cat_model_pos[1]:
                rabbit_model_pos[1] += 3
            if rabbit_model_pos[0] < cat_model_pos[0]:
                rabbit_model_pos[0] += 3
            if rabbit_model_pos[0] > cat_model_pos[0]:
                rabbit_model_pos[0] -= 3
            if rabbit.colliderect(cat) and keyboard[keys.A]:
                 rabbit_health -= 2
                 rabbit_model_pos[0] -= 100
            if rabbit_health == 0:
                rabbit_dead = True
                rabbit_health = 10
                rabbit.x = 10000
                rabbitpos[counter]["has_rabbit"] = False
            saved_rabbit_pos = rabbit_model_pos
            if not 0 < rabbit.y < HEIGHT or not 0 < rabbit.x < HEIGHT:
                break
            sleep(1/30)

def update_counter():
    global timer
    global screen_background_color
    global night_color
    global background_color
    while True:
        sleep(1/100)
        timer += 1
        if game_clock.angle > 560:
            game_clock.angle = 0
        if game_clock.angle > 270:
            screen_background_color = night_color
        if game_clock.angle > 560-100:
            screen_background_color = background_color
        if timer == 360:
            timer = 0

inventory = Inventory(inventoryslots, inventoryactor)

def pick_up_item(items_actors,entity, items_collected):
    for index, i in enumerate(items_actors):
        if i.colliderect(entity):
            if entity == cat:
                inventory.append(i, index)
                del items_actors[index]
            else:
                i.image = "cursor"
            items_collected[index] = True
    return [items_actors, items_collected]

Thread(target=update_rabbit, daemon=True).start()
Thread(target=update_counter, daemon=True).start()

        
go()