# This is importing both pygame and random
import pygame
import random

Width= 500 #tbd
Height= 500 #tbd
FPS= 30 #tbd

#this is defining some colours
Black= (0, 0, 0)
White= (255, 255, 255)
Red= (255, 0, 0)
Green= (0, 225, 0)
Blue= (0, 0, 255)

#This is initiating pygame and the pygame mixer and it creates the window size.
pygame.init()
pygame.mixer.init()
screen= pygame.display.set_mode((Width, Height))
pygame.display.set_caption("name of game")
clock= pygame.time.Clock()

#Game loop
Active= True
while Active:
    #this makes sure the game loop is staying at a constant speed
    clock.tick(FPS)
    #this for loop is processing events
    for event in pygame.event.get():
        #this is statement checks if the player has quit
        if event.type == pygame.QUIT:
            #if they have it ends the game loop
            Active= False

    screen.fill(Black)

    pygame.display.flip()

pygame.quit()