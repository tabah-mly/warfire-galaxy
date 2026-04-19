from utils.spritesheet import SpriteSheet
from utils.base_basic import BaseBasic


class Base(BaseBasic):
    def __init__(self, x, y):
        self.animator = SpriteSheet("assets/imgs/base.png", 4, 200)
        self.max_health = 300
        self.health = 300
        self.initialize(x, y)

    def draw(self, surface, camera):
        self.draw_sprite(surface, camera)
        self.draw_hp(surface)
