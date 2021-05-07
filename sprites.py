
import pygame
from Settings import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(Yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (Width/2, Height/2)
        self.pos = vec(Width/2, Height/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        Key= pygame.key.get_pressed()
        if Key[pygame.K_d]:
            self.acc.x = player_acc
        if Key[pygame.K_a]:
            self.acc.x = -player_acc
        if Key[pygame.K_a] and Key[pygame.K_LSHIFT]:
            self.acc.x = -2 * player_acc
        if Key[pygame.K_d] and Key[pygame.K_LSHIFT]:
            self.acc.x = 2 * player_acc


        self.acc += self.vel * player_fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos

