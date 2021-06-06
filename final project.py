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
    #assigning the bar variables
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


score = 0

def draw_score(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, White)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)






# this is the game class
class Game:
    #this initiates the class and creates the variables the will be used later in the class
    def __init__(self) -> object:
        #This is initiating pygame and the pygame mixer and it creates the window size
        pygame.init()
        pygame.mixer.init()
        self.screen= pygame.display.set_mode((Width, Height))

        #this mkaes the game name apear on the to of the window
        pygame.display.set_caption(Title)
        self.clock = pygame.time.Clock()
        self.Active = True
        self.load_data()
        self.level = 1


    # This function loads all the data need form the extra files we have
    def load_data(self):
        #these are just creating paths to make it easier for any computer for find the files
        game_folder = path.dirname(__file__)
        maps_folder = path.join(game_folder, 'maps')
        img_folder = path.join(game_folder, 'img')
        sprites_folder = path.join(img_folder, 'sprites')
        player_folder = path.join(img_folder, 'Hero')
        zombie_folder = path.join(img_folder,'individual enemy sprites')
        items_folder = path.join(sprites_folder, 'extra items')

        #This is getting the file for the first map, making the map and assigning its rect to a variable for later use
        self.map1 = maps(path.join(maps_folder, 'Map1.tmx'))
        self.map1_img = self.map1.Make_map()
        self.map1_rect = self.map1_img.get_rect()

        #This is getting the file for the second map, making the map and assigning its rect to a variable for later use
        self.map2 = maps(path.join(maps_folder, 'Map2.tmx'))
        self.map2_img = self.map2.Make_map()
        self.map2_rect = self.map2_img.get_rect()

        #This is getting the file for the thrid map, making the map and assigning its rect to a variable for later use
        self.map3 = maps(path.join(maps_folder, 'Map 3.tmx'))
        self.map3_img = self.map3.Make_map()
        self.map3_rect = self.map3_img.get_rect()

        #This is getting the file for the last map, making the map and assigning its rect to a variable for later use
        self.map4 = maps(path.join(maps_folder, 'Map4.tmx'))
        self.map4_img = self.map4.Make_map()
        self.map4_rect = self.map4_img.get_rect()

        # this is assigning the sprites for the character, enemies, coins and the arrow to their respective variables
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

    #this function loads the platfroms and hit boxes in the maps
    def load_map(self):
        #This if statement checks of the level variable is == 1
        if self.level == 1:
            #this for loop goes through all the data of the objects in map1
            for tile_object in self.map1.tmxdata.objects:

                #This if statement checks for platforms in the tiled map, creates a new platform and adds their values to the platfroms group
                if tile_object.name == "platform":
                    plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.platforms.add(plat_new)

                #this if statement checks for player_spawn in the tiled map and makes the the players position at the start of the level
                #the x and y coordinates at the start of the level
                if tile_object.name == "player_spawn":
                    self.player.pos = ((tile_object.x, tile_object.y))

                #this if statement checks for zombie_spawns in the tiled map and spawns zombies at those x and y cooridnates
                if tile_object.name == "zombie_spawn":
                    self.Zombies.add(Zombie(self, tile_object.x, tile_object.y ))

                #this if stamement checks for zombie barriers in the tiled map, creates a new Zombie_bar and adds their values to the Zombie_bar group
                if tile_object.name == "zombie_bar":
                    bar_new = Zombie_bar(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Zombie_bar.add(bar_new)

                #this if statement checks for exits, creates a new exit and adds their values to the exit group
                if tile_object.name == "exit":
                    exit_new = Exit(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.exit.add(exit_new)

                #this if statement checks for coin_spawn and adds their values to the coin group
                if tile_object.name == "coin_spawn":
                    self.coin.add(Coin(self, tile_object.x, tile_object.y ))

                #this if statement checks for spike in the tiled map and creates a new spike and adds it value to the spike group
                if tile_object.name == "spike":
                    Spikes_new = Spikes(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Spikes.add(Spikes_new)

        #this if statment checks if the level is equal to 2
        if self.level == 2:
            #this for loop goes through all the object data of map 2
            for tile_object in self.map2.tmxdata.objects:
                #these if statements check for the different types of objects, creates objects and adds them to their respective groups
                if tile_object.name == "platform":
                    plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.platforms.add(plat_new)

                #this if statement checks for player_spawn in the tiled map and makes the the players position at the start of the level
                #the x and y coordinates at the start of the level
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
        #this if statment checks if the level is equal to 3
        if self.level == 3:
            #this for loop goes through all the object data of map 3
            for tile_object in self.map3.tmxdata.objects:
                #these if statements check for the different types of objects, creates objects and adds them to their respective groups
                if tile_object.name == "platform":
                    plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.platforms.add(plat_new)

                #this if statement checks for player_spawn in the tiled map and makes the the players position at the start of the level
                #the x and y coordinates at the start of the level
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
        #this if statment checks if the level is equal to 4
        if self.level == 4:
            #this for loop goes through all the object data of map 4
            for tile_object in self.map4.tmxdata.objects:
                #these if statements check for the different types of objects, creates objects and adds them to their respective groups
                if tile_object.name == "platform":
                    plat_new = Platform(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.platforms.add(plat_new)

                #this if statement checks for player_spawn in the tiled map and makes the the players position at the start of the level
                #the x and y coordinates at the start of the level
                if tile_object.name == "player_spawn":
                    self.player.pos = ((tile_object.x, tile_object.y))
                if tile_object.name == "zombie_spawn":
                    self.Zombies.add(Zombie(self, tile_object.x, tile_object.y ))
                if tile_object.name == "zombie_bar":
                    bar_new = Zombie_bar(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Zombie_bar.add(bar_new)
                if tile_object.name == "exit_final":
                    exit_new = Exit_final(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.exit_final.add(exit_new)
                if tile_object.name == "coin_spawn":
                    self.coin.add(Coin(self, tile_object.x, tile_object.y ))
                if tile_object.name == "spike":
                    Spikes_new = Spikes(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                    self.Spikes.add(Spikes_new)

    #This function creates initiates all of the groups and calls on the load_map and run functions
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

    #This function is the game loop
    def run(self):
        #this while loop calls events, update and draw function at the rate of the fps
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        #This is updating all the sprites
        self.all_sprites.update()

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            #if the player does hit, the player is put at the top of the collision and it's y velocity is put to zero
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        #this updates the camera in relation to the player sprite,
        # making sure it the player stays in the middle of the camera
        self.camera.update(self.player)

        #check if zombie hits a platform - only if falling
        for i in self.Zombies:
            hits_zombie = pygame.sprite.spritecollide(i, self.platforms, False)
            if hits_zombie:
                #if the enemie does hit, the enemie is put at the top of the collision and it's y velocity is put to zero
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

            #This checks if the player hits the exit and if it does then it adds on to the level variable
            #emptiesthe all_sprites group and loads the next map
            hit_exit = pygame.sprite.spritecollide(self.player, self.exit, False)
            if hit_exit:
                self.level += 1
                self.all_sprites.empty()
                self.load_map()


            # hit_final_exit = pygame.sprite.spritecollide(self, self.game.exit_final, False)
           # if hit_final_exit:
               # self.game.Active = False


    def draw(self):
        #remouve this later
        #pygame.display.set_caption("{:.2}".format(self.clock.get_fps()))

        #This makes the screen black every frame as a way to refresh the display
        self.screen.fill(Black)

        #this checks the value of the level, and applyies the map image to the display
        if self.level == 1:
            self.screen.blit(self.map1_img, self.camera.applyRect(self.map1_rect))
        if self.level == 2:
            self.screen.blit(self.map2_img, self.camera.applyRect(self.map2_rect))
        if self.level == 3:
            self.screen.blit(self.map3_img, self.camera.applyRect(self.map3_rect))
        if self.level == 4:
            self.screen.blit(self.map4_img, self.camera.applyRect(self.map4_rect))

        #this for loop checks for zombies and draws their health and blit's all of the sprite to the display
        for sprite in self.all_sprites:
            if isinstance(sprite, Zombie):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        #this draws the player health bar to the display
        draw_player_health(self.screen, 10, 10, self.player.health / player_health)
        #these are always calling on the fade functions,
        # yet it will still work because they have conditions that need to be meet before playing
        self.player.fade_Black()
        self.player.death_Fade()

        draw_score(self.screen, str(score), 18, Width / 2, 10)



        #This flips the display every frame
        pygame.display.flip()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass

#This calls on the game class
game = Game()
game.show_start_screen()

#this is the main game loop
while game.Active:
    game.new()
    game.show_gameover_screen()

#this ends the game
pygame.quit()
