from pgzhelper import Actor
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
    def init(item_type, collected=False, hotbar_slot=0):
        self.item_type = item_type
        self.collected = collected

def pick_up_item(items_actors, entity, items_collected, inventory):
    for index, i in enumerate(items_actors):
        if i.colliderect(entity):
            if entity == cat:
                inventory.append(i, index)
                del items_actors[index]
            else:
                i.image = "cursor"
            items_collected[index] = True
    return [items_actors, items_collected]
