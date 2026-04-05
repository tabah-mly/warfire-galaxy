import pygame, sys, random
from utils.camera import Camera
from utils.game_base import GameBase
from utils.infinite_background import InfiniteBackground
from player import Player
from enemy import Enemy
from base import Base
from utils.game_over import GameOver


class Game(GameBase):
    def __init__(self, width, height, title):
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

        self.initialize()

        self.running = True
        self.game_state = "playing"

        pygame.display.set_caption(title)

        self.camera = Camera(1280, 720)
        self.background = InfiniteBackground("assets/imgs/bg.png")
        self.player = Player(400, 500)
        self.base = Base(400, 300)

        self.spawn_interval = 2000

        self.timer = 3000

        self.game_over = GameOver(width, height)

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.screen_event_listener(event)

    def restart(self):
        self.__init__(self.screen_width, self.screen_height, self.screen_title)

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

    def update(self, dt):
        if self.game_state == "win" or self.game_state == "lose":
            self.player.aim_pointer.is_active = False
            self.game_over.update(dt)
            return

        if self.game_state != "playing":
            return

        self.timer -= dt
        if self.timer <= 0:
            self.game_state = "win"
            self.timer = 0

        if self.base.health <= 0 or self.player.health <= 0:
            self.game_state = "lose"

        self.player.update(dt)
        self.base.update(dt)

        max_enemies = 8

        self.update_enemies(dt, max_enemies)
        self.update_bullets()

        self.camera.follow(self.player.rect)

    def draw(self):
        self.screen.fill((24, 20, 37))
        self.background.draw(self.screen, self.camera.offset)
        self.base.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)

        self.draw_player_health(20, 20, 300, 20)
        self.draw_base_health(20, 60, 300, 20)

        self.ui.draw(self.player, self.timer)

        if self.game_state == "win" or self.game_state == "lose":
            self.game_over.draw(self.screen, self.game_state)

    def start(self):
        while self.running:
            dt = self.clock.tick(60)

            self.event_listener()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
