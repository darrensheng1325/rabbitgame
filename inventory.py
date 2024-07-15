from pgzhelper import *
from player import cat
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
            item_num += 1
        except Exception:
            self.drop(item, index)

class item(Actor):
    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        self._flip_x = False
        self._flip_y = False
        self._scale = 1
        self._mask = None
        self._animate_counter = 0
        self.fps = 5
        self.direction = 0
        self.item_type = 0
        self.collected = False
        super().__init__(image, pos, anchor, **kwargs)
    def update_item_type(self, item_id):
        self.item_type = item_id
        self.image = f"item_{item_id}"

def pick_up_item(items_actors, entity, items_collected, inventory, score):
    for item_type, items in items_actors.items():
        for i, item in enumerate(items):
            if item.colliderect(entity):
                if entity == cat:
                    inventory.append(item, i)
                    score += 1
                    del items[i]
                else:
                    item.image = "cursor"
                items_collected[i] = True
    return [items_actors, items_collected], score
