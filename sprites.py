
import pygame
from Camera_maps import *
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
        self.pos_y = 0
        self.pos_x = 0
        self.load_data()
        self.collition= False

    def load_data(self):
        game_folder = path.dirname(__file__)
        maps_folder = path.join(game_folder, 'maps')
        self.map1= maps(path.join(maps_folder, 'Map1.tmx'))
        self.Plat_rect = []
        for tile_object in self.map1.tmxdata.objects:
            if tile_object.name == "platform":
                self.Plat_rect.append(tile_object.x)
                self.Plat_rect.append(tile_object.y)


    def update(self):
        self.ground = True
        self.rect.x += 1
        hit_y = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1

        while hit_y:
            if self.vel.y > 0:
                self.rect.bottom = hit_y[0].rect.top
                self.vel.y = 0
                self.ground = True
            if self.vel.y < 0:
                self.vel.y = 0
                self.rect.top = hit_y[0].rect.bottom
        else:
            self.ground = False
            self.acc = vec(0, player_grav)
        #
        # hit_x = pygame.sprite.spritecollide(self, self.game.platforms, False)
        # if hit_x:
        #     if self.vel.x > 0:
        #         self.acc.x = 0
        #         self.vel.x = 0
        #         self.rect.right = hit_x[0].rect.left
        #         print('Hit')
        #     if self.vel.x < 0:
        #         self.acc.x = 0
        #         self.vel.x = 0
        #         self.rect.left = hit_x[0].rect.right


        # if not self.collision():
        self.acc = vec(0, player_grav)
        Key= pygame.key.get_pressed()
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

        # self.rect.x -= 1
        # if hits and Key[pygame.K_SPACE]:
        #     self.vel.y = -20
        #
        #
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

        # Key= pygame.key.get_pressed()
        # hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        # i = 1
        # while self.Plat_rect:
        #     if self.Plat_rect[i] == self.pos_y:
        #         if self.Plat_rect[i-1] == self.pos_x or self.Plat_rect[i-1] == self.pos_x + Tilesize:
        #             self.collition = True
        #     i += 2
        # for platform in self.Plat_rect:
        #     if platform.x == self.pos.x + self.vel.x and platform.y == self.pos.y+ self.vel.y:
        #        self.collition = True
        #     self.collition = False

        # if self.collition == False:
        #     self.vel.y = 0.9
        #     if hits and Key[pygame.K_SPACE]:
        #         self.vel.y = -20
        #     if Key[pygame.K_d] and Key[pygame.K_LSHIFT]:
        #         self.vel.x = player_vel * 2
        #     if Key[pygame.K_a] and Key[pygame.K_LSHIFT]:
        #         self.vel.x = -player_vel * 2
        #     if Key[pygame.K_a]:
        #         self.vel.x = -player_vel
        #     if Key[pygame.K_d]:
        #         self.vel.x = player_vel
        #
        #     self.pos += self.vel
        #     self.rect.midbottom = self.pos


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

        hit_bar= pygame.sprite.spritecollide(self, self.game.platforms, False)

        # if hit_bar:
        #     self.acc.x = -self.acc.x
        # else:
        #     self.acc.x = Zombie_acc
        self.acc.y = Zombie_grav
        self.acc.y += self.vel.y * player_fric
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + 0.5 * self.acc.y
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

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y





