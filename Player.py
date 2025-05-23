import pygame
from Bullet import Bullet

class Player(pygame.sprite.Sprite):
    """A class the user can control"""

    def __init__(self, x, y, platform_group, portal_group, bullet_group, window_width, window_height):
        """Initialize the player"""
        super().__init__()  # Call super init

        # Set constant variables
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.8
        self.VERTICAL_JUMP_SPEED = 18
        self.STARTING_HEALTH = 100
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height

        # Animation frames
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.jump_right_sprites = []
        self.jump_left_sprites = []
        self.attack_right_sprites = []
        self.attack_left_sprites = []

        # Moving
        for i in range(1, 11):
            img = pygame.transform.scale(
                pygame.image.load(f"./assets/images/player/run/Run ({i}).png"), (64, 64)
            )
            self.move_right_sprites.append(img)
        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Idling
        for i in range(1, 11):
            img = pygame.transform.scale(
                pygame.image.load(f"./assets/images/player/idle/Idle ({i}).png"), (64, 64)
            )
            self.idle_right_sprites.append(img)
        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Jumping
        for i in range(1, 11):
            img = pygame.transform.scale(
                pygame.image.load(f"./assets/images/player/jump/Jump ({i}).png"), (64, 64)
            )
            self.jump_right_sprites.append(img)
        for sprite in self.jump_right_sprites:
            self.jump_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Attacking
        for i in range(1, 11):
            img = pygame.transform.scale(
                pygame.image.load(f"./assets/images/player/attack/Attack ({i}).png"), (64, 64)
            )
            self.attack_right_sprites.append(img)
        for sprite in self.attack_right_sprites:
            self.attack_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Load image and get rect
        self.current_sprite = 0
        self.image = self.idle_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.mask = pygame.mask.from_surface(self.image)

        # Attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group

        # Animation booleans
        self.animate_jump = False
        self.animate_fire = False

        # Load sounds
        self.jump_sound = pygame.mixer.Sound("assets/sounds/jump_sound.wav")
        self.slash_sound = pygame.mixer.Sound("assets/sounds/slash_sound.wav")
        self.portal_sound = pygame.mixer.Sound("assets/sounds/portal_sound.wav")
        self.hit_sound = pygame.mixer.Sound("assets/sounds/player_hit.wav")

        # Kinematics vectors
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.VERTICAL_ACCELERATION)

        # Set initial player values
        self.health = self.STARTING_HEALTH
        self.starting_x = x
        self.starting_y = y

    def update(self):
        """Update the player"""
        self.move()
        self.check_collisions()
        self.check_animations()

        #Update the players mask
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """Move the player"""
        #Set the acceleration vector
        self.acceleration = pygame.math.Vector2(0, self.VERTICAL_ACCELERATION)

        #If the user is pressing a key, set the x-component of the acceleration to be non-zero
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .5)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .5)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, .5)
            else:
                self.animate(self.idle_left_sprites, .5)

        #Calculate new kinematics values: (4, 1) + (2, 8) = (6, 9)
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        #Update rect based on kinematic calculations and add wrap around movement
        if self.position.x < 0:
            self.position.x = self.WINDOW_WIDTH
        elif self.position.x > self.WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        """Check for collisions with platforms and portals"""
        #Collision check between player and platforms when falling
        if self.velocity.y > 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False,
                                                             pygame.sprite.collide_mask)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.top + 5
                self.velocity.y = 0

        #Collision check between player and platform if jumping up
        if self.velocity.y < 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False,
                                                             pygame.sprite.collide_mask)
            if collided_platforms:
                self.velocity.y = 0
                while pygame.sprite.spritecollide(self, self.platform_group, False):
                    self.position.y += 1
                    self.rect.bottomleft = self.position

        #Collision check for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            #Determine which portal you are moving to
            #Left and right
            if self.position.x > self.WINDOW_WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = self.WINDOW_WIDTH - 150
            #Top and bottom
            if self.position.y > self.WINDOW_HEIGHT // 2:
                self.position.y = 64
            else:
                self.position.y = self.WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def check_animations(self):
        """Check to see if jump/fire animations should run"""
        if self.animate_jump:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites, .1)
            else:
                self.animate(self.jump_left_sprites, .1)

        if self.animate_fire:
            if self.velocity.x > 0:
                self.animate(self.attack_right_sprites, .25)
            else:
                self.animate(self.attack_left_sprites, .25)

    def jump(self):
        """Jump upwards if on a platform"""
        if pygame.sprite.spritecollide(self, self.platform_group, False):
            self.jump_sound.play()
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
            self.animate_jump = True

    def fire(self):
        """Fire a 'bullet' from a sword"""
        self.slash_sound.play()
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)
        self.animate_fire = True

    def reset(self):
        """Reset the player's position"""
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(self.starting_x, self.starting_y)
        self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        """Animate the player's actions"""
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            if self.animate_jump:
                self.animate_jump = False
            if self.animate_fire:
                self.animate_fire = False
        self.image = sprite_list[int(self.current_sprite)]
