import pygame


class EnemyBasic:
    def initialize(self, x, y):
        self.state = "idle"
        self.animator = self.animations[self.state]

        self.pos = pygame.Vector2(x, y)
        self.rect = self.animator.image.get_rect(topleft=(x, y))

        self.side_offset_player = 90
        self.side_offset_base = 40

        self.facing_right = True

        self.attack_timer = 0
        self.attacking = False

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.animator = self.animations[state]
            self.animator.reset()

    def calculate_distance(self, player, base):
        self.enemy_center_x = self.rect.centerx
        self.dist_to_player = abs(player.rect.centerx - self.enemy_center_x)

        # BASE: use edges, NOT center
        base_left = base.rect.left
        base_right = base.rect.right

        if self.enemy_center_x < base_left:
            self.dist_to_base = abs(base_left - self.enemy_center_x)
            self.base_target_x = base_left
        elif self.enemy_center_x > base_right:
            self.dist_to_base = abs(self.enemy_center_x - base_right)
            self.base_target_x = base_right
        else:
            # enemy is horizontally aligned with base (inside)
            self.dist_to_base = 0
            self.base_target_x = self.enemy_center_x

    def move(self, dt, player, base):
        if self.dist_to_base < self.dist_to_player:
            self.attack_target = base
            self.target_center_x = self.base_target_x  # edge, not center
            self.offset = self.side_offset_base  # spacing for base
        else:
            self.attack_target = player
            self.target_center_x = player.rect.centerx
            self.offset = self.side_offset_player  # spacing for player

        if self.enemy_center_x < self.target_center_x:
            self.target_x = self.target_center_x - self.offset
        else:
            self.target_x = self.target_center_x + self.offset

        self.facing_right = self.target_center_x > self.enemy_center_x

        self.moving = abs(self.target_x - self.enemy_center_x) > 1
        if self.attacking:
            self.moving = False

        if self.moving:
            self.set_state("walk")
            direction_x = 1 if self.target_x > self.enemy_center_x else -1
            self.pos.x += direction_x * self.speed * (dt / 1000.0)
        else:
            if not self.attacking:
                self.set_state("idle")

    def attack(self, dt, player, base):
        self.attack_timer -= dt
        at_attack_spot = abs(self.target_x - self.enemy_center_x) <= self.attack_range

        if at_attack_spot and self.attack_timer <= 0:
            self.attacking = True
            self.attack_timer = self.attack_cooldown
            self.set_state("attack")

        if self.state == "attack":
            last_frame = len(self.animator.frames) - 1

            if self.animator.frame_index == last_frame:

                if self.attack_target is player:
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

        self.rect.topleft = self.pos
        self.animator.update(dt)
        self.current_mask = self.animator.masks[self.animator.frame_index]

        # flip mask when needed
        if not self.facing_right:
            flipped = pygame.transform.flip(self.animator.image, True, False)
            self.current_mask = pygame.mask.from_surface(flipped)

    def draw_sprite(self, surface, camera):
        image = self.animator.image

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        self.draw_pos = self.rect.topleft - camera.offset
        surface.blit(image, self.draw_pos)

    def draw_hp(self, surface):
        # --- ENEMY HP BAR ---
        health_ratio = self.health / self.max_health

        bar_width = 100
        bar_height = 5

        bar_x = self.draw_pos.x + 150
        bar_y = self.draw_pos.y + 150  # above enemy

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
