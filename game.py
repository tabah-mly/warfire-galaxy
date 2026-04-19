import pygame, sys
from utils.game_base import GameBase
from utils.infinite_background import InfiniteBackground
from player import Player
from base import Base


class Game(GameBase):
    def __init__(self, width, height, title):
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

        self.initialize()

        self.running = True
        self.game_state = "playing"

        pygame.display.set_caption(title)

        self.background = InfiniteBackground("assets/imgs/bg.png")
        self.player = Player(400, 500)
        self.base = Base(400, 300)

        self.spawn_interval = 2000
        self.timer = 10000000
        self.max_enemies = 8

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.screen_event_listener(event)

    def update(self, dt):
        if self.update_game(dt):
            return
        self.player.update(dt)
        self.base.update(dt)
        self.update_logics(dt)

    def draw(self):
        self.screen.fill((24, 20, 37))
        self.background.draw(self.screen, self.camera.offset)
        self.base.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)
        self.draw_view()

    def start(self):
        while self.running:
            dt = self.clock.tick(60)

            self.event_listener()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
