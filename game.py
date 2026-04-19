import pygame, sys, random
from utils.camera import Camera
from utils.game_base import GameBase
from utils.infinite_background import InfiniteBackground
from player import Player

class Game(GameBase):
    def __init__(self, width, height, title):
        self.screen_width = width
        self.screen_height = height
        self.screen_title = title

        self.initialize()

        pygame.display.set_caption(title)

        self.running = True

        self.background = InfiniteBackground("assets/imgs/bg.png")
        self.camera = Camera(width, height)
        self.player = Player(width // 2, height // 2)

    def event_listener(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((24, 20, 37))
        self.background.draw(self.screen, self.camera.offset)
        self.player.draw(self.screen, self.camera)

    def start(self):
        while self.running:
            dt = self.clock.tick(60)

            self.event_listener()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
