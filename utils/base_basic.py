import pygame


class BaseBasic:
    def initialize(self, x, y):
        self.image = self.animator.image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.animator.update(dt)
        self.image = self.animator.image
        self.rect = self.image.get_rect(center=self.rect.center)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw_sprite(self, surface, camera):
        self.draw_pos = self.rect.topleft - camera.offset
        surface.blit(self.image, self.draw_pos)

    def draw_hp(self, surface):
        ratio = self.health / self.max_health
        bar_width = 200
        bar_height = 10

        bar_x = self.draw_pos.x + self.image.get_width() // 2
        bar_y = self.draw_pos.y - 30

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
