from pgzhelper import *

buttons = []

class Button(Actor):
    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        self._flip_x = False
        self._flip_y = False
        self._scale = 1
        self._mask = None
        self._animate_counter = 0
        self.fps = 5
        self.direction = 0
        super().__init__(image, pos, anchor, **kwargs)

    def hide(self):
        self.hidden = True
        
    def show(self):
        self.hidden = False
        
    def onclick(self, fun):
        global buttons
        buttons.append([self.pos, fun, self])

def on_mouse_down(pos):
    for i in buttons:
        if i[2].collidepoint_pixel(pos):
            i[1]()