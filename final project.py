# This is importing both pygame and random
import pygame
import random

Width= #tbd
Height= #tbd
FPS= #tbd

#This is initiating pygame and the pygame mixer and it creates the window size.
pygame.init()
pygame.mixer.init()
screen= pygame.display.set_mode((Width, Height))
pygame.display.set_caption("name of game")
clock= pygame.time.Clock()

#Game loop
Active= True
while Active:
