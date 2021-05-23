
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
        self.ground = True
        self.health = player_health
        self.idling = False
        self.idling_counter = 0
        self.animation_list = []

    def wallCollisions(self, platforms):
        for wall in platforms:
            if pygame.sprite.collide_rect(self, wall):
                if self.acc.x > 0:
                    self.rect.right = wall.rect.left
                    self.acc.x = 0
                    self.vel.x = 0
                if self.acc.x < 0:
                    self.rect.left = wall.rect.right
                    self.acc.x = 0
                    self.vel.x = 0


    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -40



    def update(self):
        self.rect.x += 1
        hit_y = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1

        if hit_y:
            if self.vel.y > 0:
                self.vel.y = 0
                self.rect.bottom = hit_y[0].rect.top
                self.ground = True
            if self.vel.y < 0:
                self.vel.y = 0
                self.rect.top = hit_y[0].rect.bottom
        else:
            self.ground = False

        self.acc = vec(0, player_grav)
        Key= pygame.key.get_pressed()
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.acc.y=0

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

        self.wallCollisions(self.game.platforms)
        self.acc += self.vel * player_fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        hits = pygame.sprite.spritecollide(self, self.game.Zombies, False)
        for hit in hits:
            self.health -= Zombie_damage
            hit.vel = vec(0, 0)
            if self.health <= 0:
                self.playing = False

            if hits and self.vel.x <= 0:
                self.pos += vec(Zombie_knockback, 0)
            if hits and self.vel.x >= 0:
                self.pos += vec(-Zombie_knockback, 0)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = "arrow.png"
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move arrow
        self.rect.x += (self.direction * self.speed) + screen_scroll
        # check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        # check collision with characters
        if pygame.sprite.spritecollide(player, arrow_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, arrow_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()



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
        self.vel = vec(Zombie_acc, 0)
        self.health = 50

    def wallCollisions(self, platforms):
        for wall in platforms:
            if pygame.sprite.collide_rect(self, wall):
                if self.vel.x > 0:
                    self.rect.right = wall.rect.left
                    self.vel.x *= -1
                    print('hit')
                elif self.vel.x < 0:
                    self.rect.left = wall.rect.right
                    self.vel.x *= -1
                    print('hit1')


    def update(self):

        self.rect.y += 1
        hit_y = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1

        if hit_y:
            if self.vel.y > 0:
                self.vel.y = 0
                self.rect.bottom = hit_y[0].rect.top
            if self.vel.y < 0:
                self.vel.y = 0
                self.rect.top = hit_y[0].rect.bottom

        self.vel.y = Zombie_grav
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            self.vel.y=0

        self.wallCollisions(self.game.Zombie_bar)
        self.pos += self.vel
        self.rect.midbottom = self.pos

        if self.health <= 0:
            self.kill()

    def draw_health(self):
        if self.health > 40:
            col = Green
        elif self.health > 20:
            col = Yellow
        else:
            col = Red
        width = int(self.rect.width * self.health / 100)
        self.healh_bar = pygame.Rect(0, 0, width, 7)





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


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coin
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.end = x + (Tilesize *2)
        self.pos = vec(x, y)
        self.rect.topleft = self.pos






