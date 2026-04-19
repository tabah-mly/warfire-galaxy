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
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_a]:
            self.vel_x = -self.speed

        if keys[pygame.K_d]:
            self.vel_x = self.speed

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_force
            self.on_ground = False

    def update(self, dt):
        self.handle_input()
        self.handle_ground(dt, 500)
        self.handle_animation(dt)
        self.handle_attack(dt)
