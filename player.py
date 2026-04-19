import pygame
from utils.player_basic import PlayerBasic
from utils.spritesheet import SpriteSheet


class Player(PlayerBasic):
    def __init__(self, x, y):
        self.animations = {
            "idle": SpriteSheet("assets/imgs/player_idle.png", 6, 200),
            "walk": SpriteSheet("assets/imgs/player_walk.png", 6, 120),
            "jump": SpriteSheet("assets/imgs/player_jump.png", 6, 200),
        }

        self.state = "idle"

        self.speed = 200
        self.jump_force = 650
        self.gravity = 1200

        self.can_shoot = True
        self.shoot_cooldown = 200

        self.max_health = 100
        self.health = 100

        super().__init__(x, y)

    def handle_input(self):
        pass

    def update(self, dt):
        pass
