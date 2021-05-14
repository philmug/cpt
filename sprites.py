
import pygame
from Settings import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.pos = vec(0, 0)
        self.rect.center = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -40




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

        # collision
        collision_list = pygame.sprite.spritecollide(self, self.game.platforms, False)

        for collision in collision_list:
            if self.vel.x > 0:
                self.vel.x = 0
                self.rect.right = collision.rect.left

            elif self.vel.x < 0:
                self.vel.x = 0
                self.rect.left = collision.rect.right

        self.rect.y += self.vel.y + 0.5 * self.acc.y

        collision_list = pygame.sprite.spritecollide(self, self.game.platforms, False)

        for collision in collision_list:
            if self.vel.y > 0:
                self.vel.y = 0
                self.rect.bottom = collision.rect.top

            elif self.vel.y < 0:
                self.vel.y = 0
                self.rect.top = collision.rect.bottom



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

        self.acc = vec(0, Zombie_grav)
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
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x * Tilesize
        self.rect.y = y * Tilesize







