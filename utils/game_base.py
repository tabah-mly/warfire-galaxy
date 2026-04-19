import pygame, sys, random
from enemy import Enemy
from utils.camera import Camera
from utils.game_over import GameOver
from utils.ui import Ui


class GameBase:
    def initialize(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.enemies = []
        self.spawn_interval = 2000
        self.spawn_timer = 0

        self.bullets = []

        self.ui = Ui(self.screen)
        self.game_over = GameOver(self.screen_width, self.screen_height)
        self.camera = Camera(self.screen_width, self.screen_height)

    def spawn_enemy_offscreen(self):
        cam_x = self.camera.offset.x

        if random.random() < 0.5:
            spawn_x = cam_x - random.randint(300, 600)
        else:
            spawn_x = cam_x + self.screen_width + random.randint(300, 600)

        enemy = Enemy(spawn_x)
        self.enemies.append(enemy)

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

    def screen_event_listener(self, event):
        if self.game_state == "win" or self.game_state == "lose":
            if self.game_over.handle_event(event):
                self.restart()

        if self.game_state == "upgrade":
            print("UPGRADE")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if self.game_state == "playing":
                    self.game_state = "upgrade"
                elif self.game_state == "upgrade":
                    self.game_state = "playing"

    def update_game(self, dt):
        if self.game_state == "win" or self.game_state == "lose":
            self.player.aim_pointer.is_active = False
            self.game_over.update(dt)
            return True

        if self.game_state != "playing":
            return True

        self.timer -= dt
        if self.timer <= 0:
            self.game_state = "win"
            self.timer = 0

        if self.base.health <= 0 or self.player.health <= 0:
            self.game_state = "lose"

    def update_logics(self, dt):
        self.update_enemies(dt, self.max_enemies)
        self.update_bullets()
        self.camera.follow(self.player.rect)

    def draw_view(self):
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)

        self.draw_player_health(20, 20, 300, 20)
        self.draw_base_health(20, 60, 300, 20)

        self.ui.draw(self.player, self.timer)

        if self.game_state == "win" or self.game_state == "lose":
            self.game_over.draw(self.screen, self.game_state)

    def restart(self):
        self.__init__(self.screen_width, self.screen_height, self.screen_title)
