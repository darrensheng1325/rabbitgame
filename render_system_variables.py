camerascrollx = 0
camerascrolly = 0
class MapPosition:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return str((self.x, self.y))