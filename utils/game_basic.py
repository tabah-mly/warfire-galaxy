import pygame, sys, random
from utils.camera import Camera
from utils.infinite_background import InfiniteBackground
from player import Player


class GameBasic:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.enemies = []
        self.spawn_interval = 2000
        self.spawn_timer = 0

        self.bullets = []

    def spawn_enemy_offscreen(self):
        cam_x = self.camera.offset.x

        if random.random() < 0.5:
            spawn_x = cam_x - random.randint(300, 600)
        else:
            spawn_x = cam_x + self.screen_width + random.randint(300, 600)


    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_enemies(self, dt, max_enemies):
        if len(self.enemies) < max_enemies:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn_timer = self.spawn_interval
                self.spawn_enemy_offscreen()

        for enemy in self.enemies:
            enemy.update(dt, self.player, self.base)

    def update_bullets(self):
        for bullet in self.player.bullets:
            for enemy in self.enemies:

                local_x = int(bullet.pos.x - enemy.rect.x)
                local_y = int(bullet.pos.y - enemy.rect.y)

                if 0 <= local_x < enemy.rect.width and 0 <= local_y < enemy.rect.height:

                    if enemy.current_mask.get_at((local_x, local_y)):
                        enemy.take_damage(10)
                        bullet.dead = True

        self.player.bullets = [
            b for b in self.player.bullets if not getattr(b, "dead", False)
        ]

        self.enemies = [e for e in self.enemies if e.health > 0]

    def draw_player_health(self, x, y, w, h):
        ratio = self.player.health / self.player.max_health

        pygame.draw.rect(self.screen, (60, 60, 60), (x, y, w, h))

        pygame.draw.rect(self.screen, (90, 200, 90), (x, y, w * ratio, h))

    def draw_base_health(self, x, y, w, h):
        pass
