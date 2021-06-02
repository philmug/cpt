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
from os import path

# player health
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
        #This is initiating pygame and the pygame mixer and it creates the window size
        pygame.init()
        pygame.mixer.init()
        self.screen= pygame.display.set_mode((Width, Height))
        pygame.display.set_caption(Title)
        self.clock = pygame.time.Clock()
        self.Active = True
        self.load_data()
        self.level = 1



    def load_data(self):
        game_folder = path.dirname(__file__)
        maps_folder = path.join(game_folder, 'maps')
        img_folder = path.join(game_folder, 'img')
        sprites_folder = path.join(img_folder, 'sprites')
        player_folder = path.join(img_folder, 'Hero')
        zombie_folder = path.join(img_folder,'individual enemy sprites')
        items_folder = path.join(sprites_folder, 'extra items')

        self.map1 = maps(path.join(maps_folder, 'Map1.tmx'))
        self.map1_img = self.map1.Make_map()
        self.map1_rect = self.map1_img.get_rect()

        self.map2 = maps(path.join(maps_folder, 'Map2.tmx'))
        self.map2_img = self.map2.Make_map()
        self.map2_rect = self.map2_img.get_rect()

        self.map3 = maps(path.join(maps_folder, 'Map 3.tmx'))
        self.map3_img = self.map3.Make_map()
        self.map3_rect = self.map3_img.get_rect()

        self.map4 = maps(path.join(maps_folder, 'Map4.tmx'))
        self.map4_img = self.map4.Make_map()
        self.map4_rect = self.map4_img.get_rect()

        self.player_img = pygame.image.load(path.join(player_folder, 'player_right1.png')).convert_alpha()
        self.zombie_img = pygame.image.load(path.join(zombie_folder, 'enemy_left1.png')).convert_alpha()
        self.coin_img = pygame.image.load(path.join(items_folder, 'coin_gold.png')).convert_alpha()
        self.bullet_img = pygame.image.load(path.join(items_folder, 'arrow_silver.png')).convert_alpha()

        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, Hs_File), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def load_map(self):
        if self.level == 1:
            for tile_object in self.map1.tmxdata.objects:
                if tile_object.name == "platform":
                    plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.platforms.add(plat_new)
                if tile_object.name == "player_spawn":
                    self.player.pos = ((tile_object.x, tile_object.y))
                if tile_object.name == "zombie_spawn":
                    self.Zombies.add(Zombie(self, tile_object.x, tile_object.y ))
                if tile_object.name == "zombie_bar":
                    bar_new = Zombie_bar(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Zombie_bar.add(bar_new)
                if tile_object.name == "exit":
                    exit_new = Exit(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.exit.add(exit_new)
                if tile_object.name == "coin_spawn":
                    self.coin.add(Coin(self, tile_object.x, tile_object.y ))
                if tile_object.name == "spike":
                    Spikes_new = Spikes(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Spikes.add(Spikes_new)

        if self.level == 2:
            for tile_object in self.map2.tmxdata.objects:
                if tile_object.name == "platform":
                    plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.platforms.add(plat_new)
                if tile_object.name == "player_spawn":
                    self.player.pos = ((tile_object.x, tile_object.y))
                if tile_object.name == "zombie_spawn":
                    self.Zombies.add(Zombie(self, tile_object.x, tile_object.y ))
                if tile_object.name == "zombie_bar":
                    bar_new = Zombie_bar(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Zombie_bar.add(bar_new)
                if tile_object.name == "exit":
                    exit_new = Exit(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.exit.add(exit_new)
                if tile_object.name == "coin_spawn":
                    self.coin.add(Coin(self, tile_object.x, tile_object.y ))
                if tile_object.name == "spike":
                    Spikes_new = Spikes(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Spikes.add(Spikes_new)

        if self.level == 3:
            for tile_object in self.map3.tmxdata.objects:
                if tile_object.name == "platform":
                    plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.platforms.add(plat_new)
                if tile_object.name == "player_spawn":
                    self.player.pos = ((tile_object.x, tile_object.y))
                if tile_object.name == "zombie_spawn":
                    self.Zombies.add(Zombie(self, tile_object.x, tile_object.y ))
                if tile_object.name == "zombie_bar":
                    bar_new = Zombie_bar(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Zombie_bar.add(bar_new)
                if tile_object.name == "exit":
                    exit_new = Exit(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.exit.add(exit_new)
                if tile_object.name == "coin_spawn":
                    self.coin.add(Coin(self, tile_object.x, tile_object.y ))
                if tile_object.name == "spike":
                    Spikes_new = Spikes(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Spikes.add(Spikes_new)

        if self.level == 4:
            for tile_object in self.map4.tmxdata.objects:
                if tile_object.name == "platform":
                    plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.platforms.add(plat_new)
                if tile_object.name == "player_spawn":
                    self.player.pos = ((tile_object.x, tile_object.y))
                if tile_object.name == "zombie_spawn":
                    self.Zombies.add(Zombie(self, tile_object.x, tile_object.y ))
                if tile_object.name == "zombie_bar":
                    bar_new = Zombie_bar(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Zombie_bar.add(bar_new)
                if tile_object.name == "exit_final":
                    exit_new = Exit(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.exit_final.add(exit_new)
                if tile_object.name == "coin_spawn":
                    self.coin.add(Coin(self, tile_object.x, tile_object.y ))
                if tile_object.name == "spike":
                    Spikes_new = Spikes(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Spikes.add(Spikes_new)

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.Walls = pygame.sprite.Group()
        self.Zombie_bar = pygame.sprite.Group()
        self.Zombies = pygame.sprite.Group()
        self.exit = pygame.sprite.Group()
        self.exit_final = pygame.sprite.Group()
        self.coin = pygame.sprite.Group()
        self.Spikes = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.camera = camera(Width, Height)
        self.load_map()
        self.run()


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
                self.level += 1
                self.all_sprites.empty()
                self.load_map()


    def draw(self):
        #remouve this later
        #pygame.display.set_caption("{:.2}".format(self.clock.get_fps()))


        self.screen.fill(Black)
        if self.level == 1:
            self.screen.blit(self.map1_img, self.camera.applyRect(self.map1_rect))
        if self.level == 2:
            self.screen.blit(self.map2_img, self.camera.applyRect(self.map2_rect))
        if self.level == 3:
            self.screen.blit(self.map3_img, self.camera.applyRect(self.map3_rect))
        if self.level == 4:
            self.screen.blit(self.map4_img, self.camera.applyRect(self.map4_rect))

        for sprite in self.all_sprites:
            if isinstance(sprite, Zombie):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_health(self.screen, 10, 10, self.player.health / player_health)
        self.player.fade_Black()
        self.player.death_Fade()
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
