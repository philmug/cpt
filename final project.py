# This is importing both pygame and random.
import pygame
import random
import sys
#This imports everything from the settings file and sprites file
from Settings import *
from sprites import *

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
        pass


    def new(self):
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

        if self.player.rect.right >= 5*Width/6:
            self.player.pos.x -= abs(self.player.vel.x)
        if self.player.rect.left <= Width/6:
            self.player.pos.x += abs(self.player.vel.x)
        if self.player.rect.bottom <= 14*Height/15:
            self.player.pos.y += abs(self.player.vel.y)
        if self.player.rect.top >= Height/6:
            self.player.pos.y -= abs(self.player.vel.y)



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
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass


game= Game()
game.show_start_screen()
while game.Active:
    game.new()
    game.show_gameover_screen()

pygame.quit()


