import pygame
from pygame import mixer
import random
import os
import csv

#This imports everything from the settings file and sprites file
from Settings import *
from sprites import *
from os import path
from Camera_maps import *

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    Bar_length = 100
    Bar_height = 20
    fill = pct * Bar_length
    outline_rect = pygame.Rect(x, y, Bar_length, Bar_height)
    fill_rect = pygame.Rect(x, y, fill, Bar_height)
    if pct > 100:
        col = Green
    elif pct > 60:
        col = Yellow
    else:
        col = Red
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, White, outline_rect, 2)


class Game:
    def __init__(self) -> object:
        #This is initiating pygame and the pygame mixer and it creates the window size.
        pygame.init()
        pygame.mixer.init()
        self.screen= pygame.display.set_mode((Width, Height))
        pygame.display.set_caption(Title)
        self.clock= pygame.time.Clock()
        self.Active = True
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        maps_folder = path.join(game_folder, 'maps')
        img_folder = path.join(game_folder, 'img')
        player_folder = path.join(img_folder, 'individual chracter sprites')
        zombie_folder = path.join(img_folder,'individual enemy sprites')
        self.map1= maps(path.join(maps_folder, 'Map1.tmx'))
        self.map_img = self.map1.Make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pygame.image.load(path.join(player_folder, 'player_right1.png')).convert_alpha()
        self.zombie_img = pygame.image.load(path.join(zombie_folder, 'enemy_left1.png')).convert_alpha()



    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.Walls = pygame.sprite.Group()
        self.Zombie_bar = pygame.sprite.Group()
        self.Zombies = pygame.sprite.Group()
        self.exit = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.Plat_rect = []
        for tile_object in self.map1.tmxdata.objects:
            if tile_object.name == "platform":
                plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.platforms.add(plat_new)
                self.Plat_rect.append(pygame.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == "player_spawn":
                self.player.pos = ((tile_object.x, tile_object.y))
            if tile_object.name == "zombie_spawn":
                self.Zombies.add(Zombie(self, tile_object.x, tile_object.y ))
            if tile_object.name == "zombie_bar":
                bar_new= Zombie_bar(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.Zombie_bar.add(bar_new)
            if tile_object.name == "exit":
                exit_new= Exit(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.exit.add(exit_new)
            if tile_object.name == "wall":
                wall_new = Wall(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.Walls.add(wall_new)

        self.camera = camera(Width, Height)
        self.run()
        return self.Plat_rect



    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):

        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        self.camera.update(self.player)

        #check if zombie hits a platform - only if falling
        for i in self.Zombies:
            hits_zombie = pygame.sprite.spritecollide(i, self.platforms, False)
            if hits_zombie:
                i.pos.y = hits_zombie[0].rect.top
                i.vel.y = 0

        hits = pygame.sprite.groupcollide(self.Zombies, self.Sword, False, True)
        for hit in hits:
            hit.health -= Sword_damage
            hit.vel = vec(0, 0)




    def events(self):
        #this for loop is processing events
        for event in pygame.event.get():
            #this is statement checks if the player has quit
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                #if they have it ends the game loop
                self.Active= False
            hit_exit = pygame.sprite.spritecollide(self.player, self.exit, False)
            if hit_exit:
                pygame.quit()

    def draw_grid(self):
        for x in range(0, Width, Tilesize):
            pygame.draw.line(self.screen, Lightgrey, (x,0), (x,Height))
        for y in range(0, Height, Tilesize):
            pygame.draw.line(self.screen, Lightgrey, (0, y), (Width,y))


    def draw(self):
        #remouve this later
        pygame.display.set_caption("{:.2}".format(self.clock.get_fps()))


        self.screen.fill(Black)
        self.draw_grid()
        self.screen.blit(self.map_img, self.camera.applyRect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Zombies):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_health(self.screen, 10, 10, self.player.health / player_health)
        pygame.display.flip()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass

game = Game()
game.show_start_screen()
while game.Active:
    game.new()
    game.show_gameover_screen()

pygame.quit()
