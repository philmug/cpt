
import pygame
from Settings import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(Yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (Width/2, Height/2)
        self.pos = vec(Width/2, Height/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -40

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
            return False


    def update(self):
        self.acc = vec(0, player_grav)
        Key= pygame.key.get_pressed()
        if Key[pygame.K_d]:
            self.acc.x = player_acc
            self.image = pygame.transform.flip(self.image, True, False)
        if Key[pygame.K_a]:
            self.acc.x = -player_acc
            self.image = pygame.transform.flip(self.image, True, False)
        if Key[pygame.K_a] and Key[pygame.K_LSHIFT]:
            self.acc.x = -2 * player_acc
        if Key[pygame.K_d] and Key[pygame.K_LSHIFT]:
            self.acc.x = 2 * player_acc



        self.acc += self.vel * player_fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

class Zombie(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.Zombies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(Blue)
        self.rect = self.image.get_rect()
        self.rect.center = (Width/2, Height/2)
        self.pos = vec(Width/2, Height/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):

        self.acc = vec(0, player_grav)
        self.acc += self.vel * player_fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface
        self.image.fill((Green))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * Tilesize
        self.rect.y = y * Tilesize

    def update(self):

        self.acc = vec(0, Zombie_grav)
        self.acc += self.vel * player_fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos




