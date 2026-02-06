import pygame


class TrailParticle:
    def __init__(self, pos, life=100):
        self.pos = pygame.Vector2(pos)
        self.life = life
        self.max_life = life
        self.size = 4

    def update(self, dt):
        self.life -= dt
        if self.life < 0:
            self.life = 0

    def is_dead(self):
        return self.life <= 0

    def draw(self, surface, camera):
        alpha = int((self.life / self.max_life) * 255)

        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(
            surf,
            (255, 255, 255, alpha),
            (self.size // 2, self.size // 2),
            self.size // 2,
        )

        screen_pos = self.pos - camera.offset
        surface.blit(
            surf,
            (screen_pos.x - self.size // 2, screen_pos.y - self.size // 2),
        )
