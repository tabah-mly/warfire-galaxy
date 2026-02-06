import pygame
from utils.trail_particle import TrailParticle


class Bullet:
    def __init__(self, pos, direction, speed=500):
        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(direction).normalize()
        self.speed = speed
        self.radius = 5

        self.trails = []
        self.trail_timer = 0
        self.trail_interval = 20

    def update(self, dt):
        self.pos += self.dir * self.speed * (dt / 1000.0)

        self.trail_timer -= dt
        if self.trail_timer <= 0:
            self.trail_timer = self.trail_interval
            self.trails.append(TrailParticle(self.pos))

        for p in self.trails:
            p.update(dt)

        self.trails = [p for p in self.trails if not p.is_dead()]

    def draw(self, surface, camera):

        for p in self.trails:
            p.draw(surface, camera)

        screen_pos = self.pos - camera.offset
        pygame.draw.circle(surface, (255, 255, 255), screen_pos, self.radius)
