from sprite_groups import SpriteGroup
from render_system_variables import MapPosition, camerascrollx, camerascrolly

# Move cat out of the way if it collides with a wall
def move_collisions(collision_sprites, last_move, position, camerascroll):
    camerascrollx = camerascroll.x
    camerascrolly = camerascroll.y
    for collision_sprite in collision_sprites.sprites:
        if collision_sprite.collidepoint_pixel(position.x, position.y):
            if last_move == "l":
                camerascrollx -= 90
            if last_move == "r":
                camerascrollx += 90
            if last_move == "u":
                camerascrolly -= 90
            if last_move == "d":
                camerascrolly += 90
    return camerascrollx, camerascrolly