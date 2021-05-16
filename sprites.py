
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
        self.rect.x += 1
        hit_y = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        self.ground = True

        # if self.ground == False and Key[pygame.K_SPACE]:
        #     self.vel.y = -20
        #
        # if hit_y:
        #     if self.vel.y > 0:
        #         self.vel.y = 0
        #         self.rect.bottom = hit_y[0].rect.top
        #         self.ground = True
        #     if self.vel.y < 0:
        #         self.vel.y = 0
        #         self.rect.top = hit_y[0].rect.bottom
        # else:
        #     self.ground = False

        if self.vel.y > 0:
            hit_y = pygame.sprite.spritecollide(self, self.game.platforms, False)
            if hit_y:
                self.vel.y = 0
        # if not self.collision():
        self.acc = vec(0, player_grav)
        Key= pygame.key.get_pressed()
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits and Key[pygame.K_SPACE]:
            self.vel.y = -20


        if Key[pygame.K_d] and Key[pygame.K_LSHIFT]:
            self.acc.x = player_acc * 2
        if Key[pygame.K_a] and Key[pygame.K_LSHIFT]:
            self.acc.x = -player_acc * 2
        if Key[pygame.K_a]:
            self.acc.x = -player_acc
        if Key[pygame.K_d]:
            self.acc.x = player_acc

        self.acc += self.vel * player_fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    # def collision(self):
    #     for platform in self.game.platforms:
    #         if platform.x == self.x + self.vel.x and platform.y == self.y + self.vel.y:
    #             return True
    #
    #         return False
    #     for i in self.game.platforms:
    #         hit_x = pygame.sprite.spritecollide(self, self.game.platforms, False)
    #         if hit_x:
    #             if self.vel.x > 0:
    #                 self.acc.x = 0
    #                 self.vel.x = 0
    #                 self.rect.right = hit_x[0].rect.left
    #                 print('Hit')
    #             if self.vel.x < 0:
    #                 self.acc.x = 0
    #                 self.vel.x = 0
    #                 self.rect.left = hit_x[0].rect.right



class Zombie(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.Zombies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombie_img
        self.rect = self.image.get_rect()
        self.end = x + (Tilesize *2)
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.path= [x, self.end]

    def update(self):

        self.acc.y = Zombie_grav
        self.acc.y += self.vel.y * player_fric
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        if self.pos.x <= self.path[0]:
            self.acc.x = 0.5
        elif self.pos.x >= self.path[1]:
            self.acc.x = -0.5
        self.acc.x += self.vel.x * player_fric
        self.vel.x += self.acc.x
        self.pos.x += self.vel.x + 0.5 * self.acc.x



        self.rect.midbottom = self.pos


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Zombie_bar(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y







