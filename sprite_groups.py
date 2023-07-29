from pgzero.actor import Actor
class SpriteGroup:
    def __init__(self):
        self.sprites = []
    def draw(self):
        for actor in self.sprites:
            actor.draw()
    def AddSprite(self, sprite):
        self.sprites.append(sprite)
    def DeleteSprite(self, sprite):
        self.sprites.remove(sprite)
    def GetSprite(self, index):
        return self.sprites[index]