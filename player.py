import pygame
from utils.bullet import Bullet
from utils.player_basic import PlayerBasic
from utils.spritesheet import SpriteSheet
from utils.pointer import Pointer

class Player(PlayerBasic):
    def __init__(self, x, y):
        self.animations = {
            "idle": SpriteSheet("assets/imgs/player_idle.png", 6, 200),
            "walk": SpriteSheet("assets/imgs/player_walk.png", 6, 200),
            "jump": SpriteSheet("assets/imgs/player_jump.png", 6, 200),
        }

        self.state = "idle"

        self.speed = 200
        self.jump_force = 65
        self.gravity = 1200

        self.health = 100

        super().__init__(x, y)

    def handle_input(self):
        pass

    def update(self):
        pass