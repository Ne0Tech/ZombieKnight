import pygame
import random


class Ruby(pygame.sprite.Sprite):
    """A class the player must collect to earn points and health"""

    def __init__(self, platform_group, portal_group, window_width, window_height):
        """Initialize the ruby"""
        super().__init__()

        # Set constant variables
        self.VERTICAL_ACCELERATION = 3
        self.HORIZONTAL_VELOCITY = 5
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height

        # Animation frames
        self.ruby_sprites = []

        # Load all rotation sprites
        self.ruby_sprites.append(
            pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile000.png"), (64, 64)))
        self.ruby_sprites.append(
            pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile001.png"), (64, 64)))
        self.ruby_sprites.append(
            pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile002.png"), (64, 64)))
        self.ruby_sprites.append(
            pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile003.png"), (64, 64)))
        self.ruby_sprites.append(
            pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile004.png"), (64, 64)))
        self.ruby_sprites.append(
            pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile005.png"), (64, 64)))
        self.ruby_sprites.append(
            pygame.transform.scale(pygame.image.load("./assets/images/ruby/tile006.png"), (64, 64)))

        # Load image and get rect
        self.current_sprite = 0
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (window_width // 2, 100)

        # Attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group


        self.portal_sound = pygame.mixer.Sound("assets/sounds/portal_sound.wav")

        # Kinematic vectors
        self.position = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.velocity = pygame.math.Vector2(
            random.choice([-1 * self.HORIZONTAL_VELOCITY, self.HORIZONTAL_VELOCITY]),
            0
        )
        self.acceleration = pygame.math.Vector2(0, self.VERTICAL_ACCELERATION)

    def update(self):
        """Update the ruby"""
        self.animate(self.ruby_sprites, 0.25)
        self.move()
        self.check_collisions()

    def move(self):
        """Move the ruby"""

        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # Window wrapping
        if self.position.x < 0:
            self.position.x = self.WINDOW_WIDTH
        elif self.position.x > self.WINDOW_WIDTH:
            self.position.x = 0


        self.rect.bottomleft = self.position

    def check_collisions(self):
        """Check for collisions with platforms and portals"""

        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0


        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()

            if self.position.x > self.WINDOW_WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = self.WINDOW_WIDTH - 150

            if self.position.y > self.WINDOW_HEIGHT // 2:
                self.position.y = 64
            else:
                self.position.y = self.WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        """Animate the ruby"""
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]
