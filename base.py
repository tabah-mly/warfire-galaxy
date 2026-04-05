import pygame
from utils.spritesheet import SpriteSheet


class Base:
    def __init__(self, x, y):
        self.animator = SpriteSheet("assets/imgs/base.png", 4, 200)

        self.image = self.animator.image
        self.rect = self.image.get_rect(center=(x, y))

        self.max_health = 300
        self.health = 300

    def update(self, dt):
        self.animator.update(dt)
        self.image = self.animator.image
        self.rect = self.image.get_rect(center=self.rect.center)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw(self, surface, camera):
        draw_pos = self.rect.topleft - camera.offset
        surface.blit(self.image, draw_pos)

        ratio = self.health / self.max_health
        bar_width = 200
        bar_height = 10

        bar_x = draw_pos.x + self.image.get_width() // 2
        bar_y = draw_pos.y - 30

        pygame.draw.rect(
            surface,
            (50, 50, 50),
            (bar_x - bar_width // 2, bar_y, bar_width, bar_height),
        )
        pygame.draw.rect(
            surface,
            (78, 185, 147),
            (bar_x - bar_width // 2, bar_y, bar_width * ratio, bar_height),
        )
