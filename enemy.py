import pygame
from utils.spritesheet import SpriteSheet


class Enemy:
    def __init__(self, x):
        self.animations = {
            "idle": SpriteSheet("assets/imgs/enemy_idle.png", 6, 200),
            "walk": SpriteSheet("assets/imgs/enemy_walk.png", 6, 120),
            "attack": SpriteSheet("assets/imgs/enemy_attack.png", 6, 150),
        }

        self.state = "idle"
        self.animator = self.animations[self.state]

        y = 116.5
        self.pos = pygame.Vector2(x, y)
        self.rect = self.animator.image.get_rect(topleft=(x, y))

        self.speed = 80
        self.side_offset_player = 90
        self.side_offset_base = 40

        self.facing_right = True

        self.attack_range = 30
        self.attack_cooldown = 800
        self.attack_timer = 0
        self.attacking = False

        self.max_health = 30
        self.health = 30

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def update(self, dt, player, base):
        enemy_center_x = self.rect.centerx

        # --------------------------------------
        # 1) CALCULATE DISTANCES TO TARGETS
        # --------------------------------------
        dist_to_player = abs(player.rect.centerx - enemy_center_x)

        # BASE: use edges, NOT center
        base_left = base.rect.left
        base_right = base.rect.right

        if enemy_center_x < base_left:
            dist_to_base = abs(base_left - enemy_center_x)
            base_target_x = base_left
        elif enemy_center_x > base_right:
            dist_to_base = abs(enemy_center_x - base_right)
            base_target_x = base_right
        else:
            # enemy is horizontally aligned with base (inside)
            dist_to_base = 0
            base_target_x = enemy_center_x

        # --------------------------------------
        # 2) PICK CLOSEST TARGET
        # --------------------------------------
        if dist_to_base < dist_to_player:
            attack_target = base
            target_center_x = base_target_x  # edge, not center
            offset = self.side_offset_base  # spacing for base
        else:
            attack_target = player
            target_center_x = player.rect.centerx
            offset = self.side_offset_player  # spacing for player

        # --------------------------------------
        # 3) COMPUTE IDEAL STAND POSITION
        # --------------------------------------
        if enemy_center_x < target_center_x:
            target_x = target_center_x - offset
        else:
            target_x = target_center_x + offset

        # --------------------------------------
        # 4) FACING DIRECTION
        # --------------------------------------
        self.facing_right = target_center_x > enemy_center_x

        # --------------------------------------
        # 5) MOVEMENT
        # --------------------------------------
        moving = abs(target_x - enemy_center_x) > 1
        if self.attacking:
            moving = False

        if moving:
            self.set_state("walk")
            direction_x = 1 if target_x > enemy_center_x else -1
            self.pos.x += direction_x * self.speed * (dt / 1000.0)
        else:
            if not self.attacking:
                self.set_state("idle")

        # --------------------------------------
        # 6) ATTACK LOGIC
        # --------------------------------------
        self.attack_timer -= dt
        at_attack_spot = abs(target_x - enemy_center_x) <= self.attack_range

        if at_attack_spot and self.attack_timer <= 0:
            self.attacking = True
            self.attack_timer = self.attack_cooldown
            self.set_state("attack")

        # --------------------------------------
        # 7) DEAL DAMAGE AT END OF ATTACK
        # --------------------------------------
        if self.state == "attack":
            last_frame = len(self.animator.frames) - 1

            if self.animator.frame_index == last_frame:

                if attack_target is player:
                    # player hit detection (simple)
                    if abs(self.rect.centerx - player.rect.centerx) < 120:
                        player.take_damage(10)

                else:  # attack_target is BASE
                    enemy_left = self.rect.left
                    enemy_right = self.rect.right
                    base_left = base.rect.left
                    base_right = base.rect.right

                    # Enemy colliding with base edges
                    if enemy_right >= base_left - 5 and enemy_left < base_left:
                        base.take_damage(10)

                    elif enemy_left <= base_right + 5 and enemy_right > base_right:
                        base.take_damage(10)

                self.attacking = False


        # --------------------------------------
        # 8) UPDATE SPRITE & MASK
        # --------------------------------------
        self.rect.topleft = self.pos
        self.animator.update(dt)
        self.current_mask = self.animator.masks[self.animator.frame_index]

        # flip mask when needed
        if not self.facing_right:
            flipped = pygame.transform.flip(self.animator.image, True, False)
            self.current_mask = pygame.mask.from_surface(flipped)

    def draw(self, surface, camera):
        image = self.animator.image

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        draw_pos = self.rect.topleft - camera.offset
        surface.blit(image, draw_pos)

        # --- ENEMY HP BAR ---
        health_ratio = self.health / self.max_health

        bar_width = 100
        bar_height = 5

        bar_x = draw_pos.x + 150
        bar_y = draw_pos.y + 150  # above enemy

        # HP background
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # HP foreground
        pygame.draw.rect(
            surface, (200, 50, 50), (bar_x, bar_y, bar_width * health_ratio, bar_height)
        )

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
