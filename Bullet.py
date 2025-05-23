import pygame


class Bullet(pygame.sprite.Sprite):
    """A projectile launched by the player"""

    def __init__(self, x, y, bullet_group, player):
        """Initialize the bullet"""
        super().__init__()

        # Set constant variables
        self.VELOCITY = 20
        self.RANGE = 500

        # Load image and get rect
        if player.velocity.x > 0:
            self.image = pygame.transform.scale(pygame.image.load("./assets/images/player/slash.png"), (32, 32))
        else:
            self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("./assets/images/player/slash.png"), True, False), (32, 32))
            self.VELOCITY = -1 * self.VELOCITY

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.starting_x = x

        bullet_group.add(self)

    def update(self):
        """Update the bullet"""
        # NOTE NOTE NOTE THIS: When I say add to y the value of x this means y += x or y = y + x
        self.rect.x += self.VELOCITY

        #If the bullet has passed the range, kill it
        if abs(self.rect.x - self.starting_x) > self.RANGE:
            self.kill()
