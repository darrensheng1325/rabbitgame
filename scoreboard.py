from player import max_cat_health
cat_health = max_cat_health
def check_game_over(cat_health):
    game_over = False
    if cat_health <= 0:
        game_over = True
    return game_over