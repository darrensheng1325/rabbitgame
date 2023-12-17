from pgzrun import *
from random import *
from time import sleep
from threading import Thread
from buttons import Button, TextButton, mouse_cursor
from sprite_groups import SpriteGroup
from inventory import *
from scoreboard import cat_health, check_game_over
from player import max_cat_health
from collision import move_collisions
from clock import *
from render_system_variables import MapPosition
from pgzhelper import *
from object_map import *
from controls import update_player_movement
from items import *
from environment import *
from config import WIDTH, HEIGHT, MAP_SIZE
from player import cat, max_cat_health
from save import write_save, load_save
from menu import *

cursor = Actor("cursor")
inventoryactor = Actor("inventory")
hud = Actor("hud")

rabbit = Actor("rabbit")
rabbitpos = []
for i in rabbit_positions:
    rabbitpos.append({"x":i[0],"y":i[1], "has_rabbit":True})
# rabbitpos = [
#     [0, 0],
#     [90, 90],
#     #[-90, 0],
#     #[-90, 90],
# ]\
saved_rabbit_pos = [0, 0]
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
inventoryslots = []
for i in range(25):
    inventoryslots.append([30*i+15, HEIGHT-30])
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
DEBUG_MODE = False
DEBUG_OUTPUT = []
paused = False

def draw():
    if not paused:
        if game_over:
            screen.draw.text("GAME OVER", ((WIDTH//2)-75, (HEIGHT//2)-60), fontsize=50)
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
            for item_type, items in collectible_items.items():
                for index, item in enumerate(items):
                    if not collectible_items_collected[index]:
                        position = items_positions[item_type][index]
                        item.x = position[0] + camerascrollx
                        item.y = position[1] + camerascrolly
                        item.draw()
            for i in inventory.items:
                i.draw()
        #    for index, i in enumerate(grass_map):
        #        i.x = grass_map_model_pos[index][0]
        #        i.y = grass_map_model_pos[index][1]
            collision_map.x, collision_map.y = camerascrollx, camerascrolly
            collision_map.draw()
            hud.draw()
            screen.draw.text(f"Health:{cat_health}",(60, 20))
        for i in buttons:
            if not i[2].hidden:
                i[2].draw()
        if DEBUG_MODE:
            screen.draw.text(f"DEBUG:{len(DEBUG_OUTPUT)}",(200, 20))
    else:
        walkable_map.draw()
        collision_map.draw()
        screen.fill(screen_background_color)
        draw_menu()
    mouse_cursor.draw()
        

def update():
    global game_over
    global camerascrollx
    global camerascrolly
    global last_move
    for index, i in enumerate(trees):
        i.x = treepos[index][0] + camerascrollx
        i.y = treepos[index][1] + camerascrolly
    game_over = check_game_over(cat_health)
    camerascrollx, camerascrolly = move_collisions(
        collision_sprites, last_move, MapPosition(WIDTH/2, HEIGHT/2), MapPosition(camerascrollx, camerascrolly))
    last_move, camerascrollx, camerascrolly = update_player_movement(camerascrollx, camerascrolly, last_move)
    
def on_key_down(key):
    global camerascrollx
    global camerascrolly
    global apples
    global apples_collected
    global last_move
    global paused
    if key == keys.P:
        apples_data = pick_up_item(collectible_items, cat, collectible_items_collected, inventory)
        apples = apples_data[0]
        apples_collected = apples_data[1]
    if key == keys.S:
        if DEBUG_MODE:
            global DEBUG_OUTPUT
            DEBUG_OUTPUT.append(cat_model_pos)
    if key == keys.E:
        paused=True

        

def update_rabbit():
    global saved_rabbit_pos
    global rabbit_dead
    global rabbit_health
    global counter
    global rabbit_model_pos
    global rabbitpos
    global cat_health
    global cat_model_pos
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

def on_mouse_move(pos):
    mouse_cursor.pos = pos

Thread(target=update_rabbit, daemon=True).start()
Thread(target=update_clock, daemon=True).start()

        
go()
if DEBUG_MODE:
    print(DEBUG_OUTPUT)
#quit()
