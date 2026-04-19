from utils.spritesheet import SpriteSheet
from utils.enemy_basic import EnemyBasic


class Enemy(EnemyBasic):
    def __init__(self, x):
        self.animations = {
            "idle": SpriteSheet("assets/imgs/enemy_idle.png", 6, 200),
            "walk": SpriteSheet("assets/imgs/enemy_walk.png", 6, 120),
            "attack": SpriteSheet("assets/imgs/enemy_attack.png", 6, 150),
        }

        y = 116.5
        self.speed = 80
        self.attack_range = 30
        self.attack_cooldown = 800
        self.max_health = 30
        self.health = 30

        self.initialize(x, y)

    def update(self, dt, player, base):
        self.calculate_distance(player, base)
        self.move(dt, player, base)
        self.attack(dt, player, base)

    def draw(self, surface, camera):
        self.draw_sprite(surface, camera)
        self.draw_hp(surface)
