from inventory import item
from environment import trees
from object_map import *
apples = [item("item_0") for i in range(len(trees)//2)]
revali_items = [item("item_1") for i in range(15)]
collectible_items = {"apples":apples, "revali_items":revali_items}
collectible_items_model_pos = [[1000, 1000] for i in range(len(collectible_items["apples"])*2)]
collectible_items_collected = [False for i in range(len(collectible_items["apples"])*2)]
items_positions = {"apples":apple_positions, "revali_items":revali_item_positions}
for item_type, item_positions in items_positions.items():
    for _ in range(100):
        item_positions.append([10000, 10000])
for position in items_positions:
    for index, i in enumerate(collectible_items):
        collectible_items_model_pos[index] = position[index]