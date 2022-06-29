import pygame, math


class AimingDot(pygame.sprite.Sprite):
    def __init__(self, distance):
        super().__init__()
        self.distance = distance
        self.image = pygame.image.load("images/sphere-19.png")
        self.image = pygame.transform.smoothscale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 650-distance)
        self.angle = 270

    def update(self, change):
        self.angle += change
        if 190 < self.angle < 350:
            r_angle = math.radians(self.angle)
            x = math.cos(r_angle)*self.distance
            y = math.sin(r_angle)*self.distance
            self.rect.center = (200+x, 650+y)
        else:
            self.angle -= change
