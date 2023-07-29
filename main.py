from pgzrun import *
from random import *
from time import sleep
from threading import Thread
from buttons import *
from sprite_groups import SpriteGroup
from inventory import *
from scoreboard import cat_health, check_game_over
from player import max_cat_health
from collision import move_collisions
from clock import *
from render_system_variables import MapPosition
from pgzhelper import *

HEIGHT = 750
WIDTH = HEIGHT
MAP_SIZE = 2700

from player import cat, max_cat_health

cursor = Actor("cursor")
inventoryactor = Actor("inventory")
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
collectible_items = [Actor("apple") for i in range(len(trees)//2)]
collectible_items_model_pos = [[100000, 100000] for i in range(len(collectible_items))]
collectible_items_collected = [False for i in range(len(collectible_items))]
inventoryslots = []
for i in range(25):
    inventoryslots.append([30*i+15, HEIGHT-30])
for index, i in enumerate(collectible_items):
    if randint(0, 1) == 1:
        collectible_items_model_pos[index] = treepos[index]
grass_map = [Actor("grass") for i in range(400)]
grass_map_model_pos = [[10000, 10000] for i in range(500)]
for i in range(500):
    grass_map_model_pos[i] = [randint(-MAP_SIZE, MAP_SIZE)]
collision_map = Actor("collision_map")
last_move = "l"
walkable_map = Actor("walkable_map")
buttons = []
game_over = False
collision_sprites = SpriteGroup()
collision_sprites.AddSprite(collision_map)
walkable_sprites = SpriteGroup()
walkable_sprites.AddSprite(walkable_map)

def draw():
    if game_over:
        screen.draw.text("GAME OVER", (WIDTH//2, HEIGHT//2), fontsize=50)
        retry_button.show()
        retry_button.draw()
    else:
        global camerascrollx
        global camerascrolly
        screen.fill(screen_background_color)
        walkable_map.pos = camerascrollx, camerascrolly
        walkable_map.draw()
        cat.draw()
        for i in trees:
            i.draw()
        rabbit.x = rabbit_model_pos[0] + camerascrollx
        rabbit.y = rabbit_model_pos[1] + camerascrolly
        
        if rabbit.colliderect(hud):
            rabbit.draw()
        game_clock.draw()
        hud.draw()
        for index, i in enumerate(collectible_items):
            if not collectible_items_collected[index]:
                i.x = collectible_items_model_pos[index][0] + camerascrollx
                i.y = collectible_items_model_pos[index][1] + camerascrolly
        for i in collectible_items:
            i.draw()
        for i in inventory.items:
            i.draw()
    #    for index, i in enumerate(grass_map):
    #        i.x = grass_map_model_pos[index][0]
    #        i.y = grass_map_model_pos[index][1]
        collision_map.x, collision_map.y = camerascrollx, camerascrolly
        collision_map.draw()
        screen.draw.text(f"Health:{cat_health}",(60, 20))
    for i in buttons:
        if not i[2].hidden:
            i[2].draw()

def update():
    global game_over
    global camerascrollx
    global camerascrolly
    for index, i in enumerate(trees):
        i.x = treepos[index][0] + camerascrollx
        i.y = treepos[index][1] + camerascrolly
    game_over = check_game_over(cat_health)
    camerascrollx, camerascrolly = move_collisions(
        collision_sprites, last_move, MapPosition(WIDTH/2, HEIGHT/2), MapPosition(camerascrollx, camerascrolly))
    
def on_key_down(key):
    global camerascrollx
    global camerascrolly
    global apples
    global apples_collected
    global last_move
    if key == keys.UP:
        camerascrolly += 90
        last_move = "u"
    if key == keys.DOWN:
        camerascrolly -= 90
        last_move = "d"
    if key == keys.LEFT:
        camerascrollx += 90
        last_move = "l"
    if key == keys.RIGHT:
        camerascrollx -= 90
        last_move = "r"
    if key == keys.P:
        apples_data = pick_up_item(collectible_items, cat, collectible_items_collected, inventory)
        apples = apples_data[0]
        apples_collected = apples_data[1]
        

def update_rabbit():
    global saved_rabbit_pos
    global rabbit_dead
    global rabbit_health
    global counter
    global rabbit_model_pos
    global rabbitpos
    global cat_health
    while True:
        counter += 1
#         cursor.x = rabbit.x + camerascrollx
#         cursor.y = rabbit.y + camerascrolly
        rabbit_dead = False
        if counter == len(rabbitpos):
            counter = 0

        sleep(1/120)
        rabbit_here = rabbitpos[counter]["has_rabbit"]
        if not hud.colliderect(rabbit) or not rabbit_here:
            rabbit_model_pos = [rabbitpos[counter]["x"], rabbitpos[counter]["y"]]
            saved_rabbit_pos = rabbit_model_pos
            continue
        if not rabbit_here:
            continue
        
        rabbit_model_pos = saved_rabbit_pos
        while rabbitpos[counter]["has_rabbit"] and not rabbit_dead:
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

            def change_pos(index, amount):
                rabbit_model_pos[index] += amount

            if rabbit.colliderect(cat):
                if keyboard.a:
                    rabbit_health -= 2
                    actions = {
                        "l": lambda: change_pos(0, -100),
                        "r": lambda: change_pos(0, 100),
                        "u": lambda: change_pos(1, -100),
                        "d": lambda: change_pos(1, 100),
                    }
                    actions[last_move]()
                else:
                    if randint(0, 25) == 0:
                        cat_health -=2


            if rabbit_health == 0:
                rabbit_dead = True
                rabbit_health = 10
                rabbit.x = 10000
                rabbitpos[counter]["has_rabbit"] = False
                break
            saved_rabbit_pos = rabbit_model_pos
            if not 0 < rabbit.y < HEIGHT or not 0 < rabbit.x < HEIGHT:
                break
            sleep(1/30)
                # print(saved_rabbit_pos)

inventory = Inventory(inventoryslots, inventoryactor)
retry_button = Button("retry_button", (WIDTH//2, HEIGHT//2))

def retry():
    global game_over
    global cat_health
    cat_health = max_cat_health
    game_over = False
retry_button.onclick(retry)

Thread(target=update_rabbit, daemon=True).start()
Thread(target=update_clock, daemon=True).start()

        
go()
quit()
