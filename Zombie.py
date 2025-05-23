import random
import pygame

from typing import cast

class Zombie(pygame.sprite.Sprite):
    """An enemy class that moves across the screen"""

    def __init__(self, platform_group, portal_group, min_speed, max_speed, window_width, window_height, fps):
        """Initialize the zombie"""
        super().__init__() # Call super init

        # Set constant variables
        self.VERTICAL_ACCELERATION = 3
        self.RISE_TIME = 2
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        self.FPS = fps

        # Animation frames
        self.walk_right_sprites = []
        self.walk_left_sprites = []
        self.die_right_sprites = []
        self.die_left_sprites = []
        self.rise_right_sprites = []
        self.rise_left_sprites = []

        gender = random.randint(0, 1)

        if gender == 0:
            # Walking
            for i in range(1, 11):
                self.walk_right_sprites.append(
                    pygame.transform.scale(
                        pygame.image.load(f"assets/images/zombie/boy/walk/Walk ({i}).png"), (64, 64)))
            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # Dying
            for i in range(1, 11):
                self.die_right_sprites.append(
                    pygame.transform.scale(
                        pygame.image.load(f"assets/images/zombie/boy/dead/Dead ({i}).png"), (64, 64)))
            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # Rising (Dead 10 to Dead 1)
            for i in range(10, 0, -1):
                self.rise_right_sprites.append(
                    pygame.transform.scale(
                        pygame.image.load(f"assets/images/zombie/boy/dead/Dead ({i}).png"), (64, 64)))
            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))
        else:
            # Walking
            for i in range(1, 11):
                self.walk_right_sprites.append(
                    pygame.transform.scale(
                        pygame.image.load(f"assets/images/zombie/girl/walk/Walk ({i}).png"), (64, 64)))
            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # Dying
            for i in range(1, 11):
                self.die_right_sprites.append(
                    pygame.transform.scale(
                        pygame.image.load(f"assets/images/zombie/girl/dead/Dead ({i}).png"), (64, 64)))
            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # Rising (Dead 10 to Dead 1)
            for i in range(10, 0, -1):
                self.rise_right_sprites.append(
                    pygame.transform.scale(
                        pygame.image.load(f"assets/images/zombie/girl/dead/Dead ({i}).png"), (64, 64)))
            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Load an image and get rect
        self.direction = random.choice([-1, 1])
        self.current_sprite = 0
        if self.direction == -1:
            self.image = self.walk_left_sprites[self.current_sprite]
        else:
            self.image = self.walk_right_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(100, self.WINDOW_WIDTH - 100), -100)

        # Attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group

        # Animation booleans
        self.animate_death = False
        self.animate_rise = False

        # Load sounds
        self.hit_sound = pygame.mixer.Sound("./assets/sounds/zombie_hit.wav")
        self.kick_sound = pygame.mixer.Sound("./assets/sounds/zombie_kick.wav")
        self.portal_sound = pygame.mixer.Sound("./assets/sounds/portal_sound.wav")

        # Kinematics vectors
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.velocity = pygame.math.Vector2(self.direction * random.randint(min_speed, max_speed), 0)
        self.acceleration = pygame.math.Vector2(0, self.VERTICAL_ACCELERATION)

        # Initial zombie values
        self.is_dead = False
        self.round_time = 0
        self.frame_count = 0

    def update(self):
        """Update the zombie"""
        self.move()
        self.check_collisions()
        self.check_animations()

        # Determine when the zombie should rise from the dead
        if self.is_dead:
            self.frame_count += 1
            if self.frame_count % self.FPS == 0:
                self.round_time += 1
                if self.round_time == self.RISE_TIME:
                    self.animate_rise = True
                    self.current_sprite = 0

    def move(self):
        """Move the zombie"""
        if not self.is_dead:
            if self.direction == -1:
                self.animate(self.walk_left_sprites, 0.5)
            else:
                self.animate(self.walk_right_sprites, 0.5)
            self.velocity += self.acceleration
            self.position += self.velocity + 0.5 * self.acceleration
            if self.position.x < 0:
                self.position.x = self.WINDOW_WIDTH
            elif self.position.x > self.WINDOW_WIDTH:
                self.position.x = 0
            self.rect.bottomleft = self.position

    def check_collisions(self):
        """Check for collisions with platforms and portals"""
        # Collision check between zombie and platforms when falling
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0

        # Collision check for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            # Determine which portal you are moving to
            # Left and right
            if self.position.x > self.WINDOW_WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = self.WINDOW_WIDTH - 150
            # Top and bottom
            if self.position.y > self.WINDOW_HEIGHT // 2:
                self.position.y = 64
            else:
                self.position.y = self.WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def check_animations(self):
        """Check to see if death/rise animations should run"""
        # Animate the zombie death
        if self.animate_death:
            if self.direction == 1:
                self.animate(self.die_right_sprites, 0.095)
            else:
                self.animate(self.die_left_sprites, 0.095)

        # Animate the zombie rise
        if self.animate_rise:
            if self.direction == 1:
                self.animate(self.rise_right_sprites, 0.095)
            else:
                self.animate(self.rise_left_sprites, 0.095)

    def animate(self, sprite_list, speed):
        """Animate the zombie's actions"""
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            if self.animate_death:
                self.current_sprite = len(sprite_list) - 1
                self.animate_death = False
            if self.animate_rise:
                self.animate_rise = False
                self.is_dead = False
                self.frame_count = 0
                self.round_time = 0

        self.image = sprite_list[int(self.current_sprite)]
