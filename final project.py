# This is importing both pygame and random.
import pygame
import random
import sys

#This imports everything from the settings file and sprites file
from Settings import *
from sprites import *
from os import path
from Camera_maps import *

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
        sprites_folder = path.join(img_folder, 'sprites')
        character_folder = path.join(sprites_folder, 'character')
        self.map1= maps(path.join(maps_folder, 'Map1.tmx'))
        self.map_img = self.map1.Make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pygame.image.load(path.join(character_folder, 'L1.png')).convert_alpha()


    def new(self):
        self.walls = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.Zombies = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.zombies = Zombie(self)
        self.all_sprites.add(self.zombies)
        p1 = Platform(0, Height - 40, Width, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)
        for tile_object in self.map1.tmxdata.objects:
            if tile_object.name == "platform":
                plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.platforms.add(plat_new)
            if tile_object.name == "player_spawn":
                self.player.pos = ((tile_object.x, tile_object.y))
        self.camera = camera(Width, Height)
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

        self.all_sprites.update()
        # check if player hits a platform - only if falling
        hits_zombie = pygame.sprite.spritecollide(self.zombies, self.platforms, False)
        if hits_zombie:
            self.zombies.pos.y = hits_zombie[0].rect.top
            self.zombies.vel.y = 0



    def events(self):
        #this for loop is processing events
        for event in pygame.event.get():
            #this is statement checks if the player has quit
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                #if they have it ends the game loop
                self.Active= False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

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
            self.screen.blit(sprite.image, self.camera.apply(sprite))
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


