import pygame
from utils.bullet import Bullet
from utils.spritesheet import SpriteSheet
from utils.pointer import Pointer


class PlayerBasic:
    def __init__(self, x, y):
        self.animator = self.animations[self.state]

        self.rect = self.animator.image.get_rect(topleft=(x, y))

        self.vel_x = 0
        self.vel_y = 0

        self.on_ground = False
        self.facing_right = True

        self.aim_pointer = Pointer(
            orbit_radius=max(self.rect.width, self.rect.height) // 2, offset=(0, 0)
        )

        self.shoot_timer = 0
        self.bullets = []

    def _update_state(self):
        if not self.on_ground:
            self.set_state("jump")
        elif self.vel_x != 0:
            self.set_state("walk")
        else:
            self.set_state("idle")

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def bullet_update(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)

    def handle_ground(self, dt):
        dt_sec = dt / 1000.0

        self.vel_y += self.gravity * dt_sec

        self.rect.x += self.vel_x * dt_sec
        self.rect.y += self.vel_y * dt_sec

        if self.rect.bottom >= 500:
            self.rect.bottom = 500
            self.vel_y = 0
            self.on_ground = True

    def draw(self, surface, camera):
        image = self.animator.image

        base_center = self.rect.center - camera.offset

        mouse_x = pygame.mouse.get_pos()[0]
        self.facing_right = mouse_x >= base_center.x

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        draw_pos = self.rect.topleft - camera.offset
        surface.blit(image, draw_pos)

        self.aim_pointer.draw(surface, base_center, self.facing_right, camera)

        for bullet in self.bullets:
            bullet.draw(surface, camera)

        self.last_pointer_pos = self.aim_pointer.pointer_pos
        self.last_direction = self.aim_pointer.direction

    def shoot(self, pointer_pos, direction):
        bullet = Bullet(pointer_pos, direction)
        self.bullets.append(bullet)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
