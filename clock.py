from time import sleep
from pgzero.actor import Actor
timer = 2
game_clock = Actor("clock")
game_clock.x = 25
game_clock.y = 25
day_in_millis = 100
night_overlay = Actor("night_overlay")
background_color = (0, 255, 255)
night_color = (0, 0, 0)
screen_background_color = "#80d402"
def update_clock():
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
        game_clock.angle = timer / day_in_millis + 180