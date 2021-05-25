import pygame
from pygame import mixer
from os import path
vec = pygame.math.Vector2

# Window settings
Width= 1000 #tbd
Height= 600 #tbd
FPS= 60 #tbd
Title= "Until Death"

#this determines the tile size
Tilesize= 32

#player properties
player_health = 100
player_acc = 0.5
player_fric = -0.12
player_image= "L1.png" #widl be something like "main_hero.png"
player_grav = 0.9
player_vel = 1

#define player actions
moving_left = False
moving_right = False
shoot = False

#Weapon settings
Sword_image = ()
Sword_speed = 500
Sword_damage = 10

#Zombie properties
Zombie_image= 0 #will be something like "zombie.png"
Zombie_acc = 0.75
Zombie_grav= 0.9
Zombie_health = 50
Zombie_damage = 2
Zombie_knockback = 2

#coin properties
coin_score = 10

#Spike properties
Spike_damage = 10

#this is defining some colours
Black= (0, 0, 0)
White= (255, 255, 255)
Red= (255, 0, 0)
Green= (0, 225, 0)
Blue= (0, 0, 255)
Yellow= (255, 255, 0)
Darkgrey= (40, 40, 40)
Lightgrey= (100, 100, 100)

#map settings
map1_height = 25 * Tilesize
map1_length = 90 * Tilesize

pygame.init()

#adds music and volume
sound = pygame.mixer.Sound('lvl1.wav')
sound.play()



