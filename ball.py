import pygame, math


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, img_path):
        super().__init__()
        self.path = img_path
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.smoothscale(self.image, (34, 34))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.speed = [0, 0]
        self.radius = 16

    def check_off_screen(self):
        if self.rect.x < 0:
            self.rect.x += 34
        elif self.rect.right > 400:
            self.rect.x -= 34

    def update(self, balls, backboard):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.rect.center = (self.x, self.y)
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed[0] *= -1
        elif self.rect.right > 400:
            self.rect.right = 400
            self.speed[0] *= -1
        hit_list = pygame.sprite.spritecollide(self, balls, False)
        if len(hit_list) > 0:
            for b in hit_list:
                if pygame.sprite.collide_circle(self, b):
                    balls.add(self)
                    if self.rect.y > b.rect.y+16:
                        self.rect.y = b.rect.y + 30
                    else:
                        self.rect.y = b.rect.y
                    if self.rect.centerx > b.rect.centerx:
                        if self.rect.y == b.rect.y:
                            self.rect.x = b.rect.x + 34
                        else:
                            self.rect.x = b.rect.x + 17
                    else:
                        if self.rect.y == b.rect.y:
                            self.rect.x = b.rect.x - 34
                        else:
                            self.rect.x = b.rect.x - 17
                    self.speed = [0, 0]
                    self.check_off_screen()
                    return True
        if self.rect.colliderect(backboard):
            self.rect.y = backboard.bottom
            self.rect.x = 7 + 34*round((self.x-7)/34)
            balls.add(self)
            self.check_off_screen()
            return True

    def set_speed(self, angle):
        angle = math.radians(angle)
        dx = math.cos(angle)*5
        dy = math.sin(angle)*5
        self.speed = [dx, dy]
