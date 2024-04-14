from pgzero.actor import Actor
from config import WIDTH, HEIGHT
cat = Actor("cat")
max_cat_health = 20
cat.y = HEIGHT/2
cat.x = WIDTH/2

class RabbitActor(Actor):
    def __init__(self):
        super().__init__("rabbit")
        self.health = 10
        self.dead = False
        self.pos = (10000, 10000)
        self.has_rabit = False
    def update(self):
        pass