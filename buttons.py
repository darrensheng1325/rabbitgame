from pgzhelper import *
from pgzero import screen

buttons = []
mouse_cursor = Actor("mouse_click_cursor")

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

class TextButton(Actor):
    def __init__(self, image, text, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        self._flip_x = False
        self._flip_y = False
        self._scale = 1
        self._mask = None
        self._animate_counter = 0
        self.fps = 5
        self.direction = 0
        self.text = text
        super().__init__(image, pos, anchor, **kwargs)

    def draw_button(self):
        screen.draw.text(text, self.pos, fontsize=10)
    def onclick(self, fun):
        global buttons
        buttons.append([self.pos, fun, self])


def on_mouse_down(pos):
    for i in buttons:
            if i[2].colliderect(mouse_cursor):
                i[1]()