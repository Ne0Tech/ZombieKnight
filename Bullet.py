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
            # TODO: just like you did in the Tile class.  store the transformed image in self.image.  The image to use is located here
            #  "./assets/images/player/slash.png"
            pass  # TODO: remove this when done.
        else:
            # almost the same as in the if part.
            self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("./assets/images/player/slash.png"), True, False), (32, 32))
            pass  # TODO: remove this when done.

        # TODO:  assign to self.rect the following  self.image.get_rect()
        # TODO: assign to self.rect.center the tuple x, y
        # TODO: assign to self.starting_x the value of x

        # TODO: call bullet_group's add method and pass in self.

    def update(self):
        """Update the bullet"""
        # NOTE NOTE NOTE THIS:  When I say add to y the value of x this means y += x or y = y + x
        # TODO: add to self.rect.x  the value of self.VELOCITY

        #If the bullet has passed the range, kill it
        if abs(self.rect.x - self.starting_x) > self.RANGE:
            self.kill()


