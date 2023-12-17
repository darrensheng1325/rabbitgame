from pgzero.keyboard import keyboard
def update_player_movement(camerascrollx, camerascrolly, last_move):
    if keyboard.up:
        camerascrolly += 5
        last_move = "u"
    if keyboard.down:
        camerascrolly -= 5
        last_move = "d"
    if keyboard.left:
        camerascrollx += 5
        last_move = "l"
    if keyboard.right:
        camerascrollx -= 5
        last_move = "r"
    return last_move, camerascrollx, camerascrolly
