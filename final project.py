# This is importing both pygame and random.
import pygame
import random
#This imports everything from the settings file and sprites file
from Settings import *
from sprites import *

class Game:
    def __init__(self):
        #This is initiating pygame and the pygame mixer and it creates the window size.
        pygame.init()
        pygame.mixer.init()
        self.screen= pygame.display.set_mode((Width, Height))
        pygame.display.set_caption(Title)
        self.clock= pygame.time.Clock()
        self.Active = True

    def new(self):
        self.all_sprites = pygame.sprite.Group()
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

    def events(self):
        #this for loop is processing events
        for event in pygame.event.get():
            #this is statement checks if the player has quit
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                #if they have it ends the game loop
                self.Active= False

    def draw(self):
        self.screen.fill(Black)
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

