from player import max_cat_health
cat_health = max_cat_health
def check_game_over(cat_health):
    game_over = False
    if cat_health <= 0:
        game_over = True
    return game_over
class Scoreboard():
    def __init__(self):
        self.score = 0
    def increment(self):
        self.score += 1
    def decrement(self):
        self.score -= 1