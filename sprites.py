#this imports pygame, everything from the camera and settings files and creating the variable that will allow us to use
#vectors
import pygame
from Camera_maps import *
from Settings import *
vec = pygame.math.Vector2

#This is the player class
class Player(pygame.sprite.Sprite):
    #this initiates the class, imports the game class and creates the variables need later in the class
    def __init__(self, game):
        #these lines add the player to the all sprites class
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        #these lines import the game class, get the player image and rect
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()

        #These lines initiate the variables need for player movemnt
        self.pos = vec(0, 0)
        self.rect.center = self.pos
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)


        #these lines initiate variables and lists need for player health, animations and fades
        self.health = player_health
        self.idling = False
        self.idling_counter = 0
        self.animation_list = []
        self.score = 0
        self.fade_complete = True
        self.death_fade_complete = True
        self.fade_counter = 0
        self.screen = pygame.display.set_mode((Width, Height))
        self.player_flip = False

    #this is the function testing horizontal collision
    def wallCollisions(self, platforms):
        #this for loop checks every wall in the platform group
        for wall in platforms:
            #this if statement is checking if the player is colliding with any walls
            if pygame.sprite.collide_rect(self, wall):
                #this if statement is checking if the player is moving right
                if self.acc.x > 0:
                    #these lines stop the player form mouving and move the rect of the player to the left of the collision
                    self.acc.x = 0
                    self.vel.x = 0
                    self.rect.right = wall.rect.left

                #this if statement is checking if the player is mouving left
                if self.acc.x < 0:
                    #these lines stop the player form mouving and move the rect of the player to the right of the collision
                    self.acc.x = 0
                    self.vel.x = 0
                    self.rect.left = wall.rect.right

    #this is the function which fades the screen to black
    def fade_Black(self):
        #this if statement is checking to make sure the animation isn't already playing
        if self.fade_complete == False:
            #this adds four to the fade counter
            self.fade_counter += 4
            #this if statement checks of the fade counter is less than the width
            if self.fade_counter <= Width:
                #These lines draw the black squares and modify their position everyframe based on the fade_counter
                pygame.draw.rect(self.screen, Black, (0 - self.fade_counter, 0, Width // 2, Height))
                pygame.draw.rect(self.screen, Black, (Width // 2 + self.fade_counter, 0, Width, Height))
                pygame.draw.rect(self.screen, Black, (0, 0 - self.fade_counter, Width, Height // 2))
                pygame.draw.rect(self.screen, Black, (0, Height // 2 +self.fade_counter, Width, Height))
            #this if statement checks of the fade counter is greater than the width
            if self.fade_counter >= Width:
                #these lines end the animation and reset the level and character
                self.fade_complete = True
                self.game.playing = False

    #this is the function for the death animation, which is a red fade down
    def death_Fade(self):
        #this if statement is checking to make sure the animation isn't already playing
        if self.death_fade_complete == False:
            #this adds four to the fade counter
            self.fade_counter += 4
            #this if statement checks of the fade counter is less than the width
            if self.fade_counter <= Width:
                #this draws a red rectangle and modifies it position based on the fade_counter
                pygame.draw.rect(self.screen, Red, (0, 0, Width, 0 + self.fade_counter))
            #this if statement checks of the fade counter is greater than the width
            if self.fade_counter >= Width:
                #these lines end the animation and reset the level and character
                self.death_fade_complete = True
                self.game.playing = False


    #this is the jump function
    def jump(self):
        #This moves the player rect by one and checks if it is hitting a platform, then moves it back
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        #if it hitting then it jumps the character
        if hits:
            self.vel.y = -40


    #this is the jump function of the player class
    def update(self):
        #This moves the player rect by one and checks if it is hitting a platform, then moves it back
        self.rect.x += 1
        hit_y = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1

        #this checks if it is colliding with a platform
        if hit_y:
            #this checks if the player is falling
            if self.vel.y > 0:
                #This stops the character and moves it to the top of the collision
                self.vel.y = 0
                self.rect.bottom = hit_y[0].rect.top
            #this checks if the player is jumping
            if self.vel.y < 0:
                #this stops the character and moves it to the bottom of the collision
                self.vel.y = 0
                self.rect.top = hit_y[0].rect.bottom

        #This adds gravity to the player's acceleration
        self.acc = vec(0, player_grav)
        #this makes a variable for the function that checks if a kay has been pressed
        Key = pygame.key.get_pressed()

        #This moves the player rect by one and checks if it is hitting a platform, then moves it back
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        #if the player is colliding with a platform then it send his y acceleration to 0 to nulify gravity
        if hits:
            self.acc.y=0

        #if the player is hiting the ground and the person playing the game preses space then the player jumps
        if hits and Key[pygame.K_SPACE]:
            self.vel.y = -20

        #these lines check for what keys the player has pressed and modify the characters accleration based on that
        if Key[pygame.K_d] and Key[pygame.K_LSHIFT]:
            self.acc.x = player_acc * 2
            self.player_flip = False
        elif Key[pygame.K_a] and Key[pygame.K_LSHIFT]:
            self.acc.x = -player_acc * 2
            self.player_flip = True
        elif Key[pygame.K_a]:
            self.acc.x = -player_acc
            self.player_flip = True
        elif Key[pygame.K_d]:
            self.acc.x = player_acc
            self.player_flip = False

        #these lines call on the horizontal collision function and calculates the players acceleration, velocity and position
        self.wallCollisions(self.game.platforms)
        self.acc += self.vel * player_fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #this move the middle bottom of the player rect to the position
        self.rect.midbottom = self.pos

        #if the player hit a zombie, then it take off a certain amount of health from the player and pushes him back
        hits = pygame.sprite.spritecollide(self, self.game.Zombies, False)
        for hit in hits:
            self.health -= Zombie_damage
            hit.vel = vec(0, 0)
            #if the player's health reaches zero and the death animation is not playing,
            # then it plays the death animation
            if self.health <= 0 and self.death_fade_complete == True:
                self.death_fade_complete = False
            if hits and self.vel.x <= 0:
                self.pos += vec(Zombie_knockback, 0)
            if hits and self.vel.x >= 0:
                self.pos += vec(-Zombie_knockback, 0)

        #this checks if the player is hitting the spikes
        # and if he is takes off a certain amount of health from the player
        Spikes_hits = pygame.sprite.spritecollide(self, self.game.Spikes, False)
        if Spikes_hits:
            self.health -= Spike_damage
            #if the player's health reaches zero and the death animation is not playing,
            # then it plays the death animation
            if self.health <= 0 and self.death_fade_complete == True:
                self.death_fade_complete = False




        #this checks if the player is colliding with a exit block and if the fade black animation is not playing
        # it resets the fade counter, adds one to the level variable, loads the next map and starts the fade animation
        hit_exit = pygame.sprite.spritecollide(self, self.game.exit, False)
        if hit_exit and self.fade_complete == True:
            self.fade_counter = 0
            self.game.highscore += self.score/ (int(self.game.time)/1000)
            self.game.level += 1
            if self.game.level < self.game.max_level:
                self.game.load_map()
                print(self.game.highscore)
                self.fade_complete = False
            elif self.game.level >= self.game.max_level:
                self.game.highscore = int(self.game.highscore)
                if self.game.highscore > self.game.score_max:
                    with open(self.game.highest_score, 'w') as f:
                        f.write(str(self.game.highscore))
                self.game.playing = False
                self.game.Active = False


        #this checks if the player hits the coin, if it does it deletes the coin and adds to the score
        coin_hits = pygame.sprite.spritecollide(self, self.game.coin, True)
        if coin_hits:
            self.score += coin_score

        self.image = pygame.transform.flip(self.game.player_img, self.player_flip, False)


class Arrow(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.game = game
        self.image = game.bullet_img
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


#this is the zombie class
class Zombie(pygame.sprite.Sprite):
    #this initiates the class and creates the variables used in the class
    def __init__(self, game, x, y):
        #this adds the zombies to the all_sprites group and the zombie group
        self.groups = game.all_sprites, game.Zombies
        pygame.sprite.Sprite.__init__(self, self.groups)

        #this gets the game class, the zombie image and rect
        self.game = game
        self.image = game.zombie_img
        self.rect = self.image.get_rect()

        #this initiates the zombie position, rect_centre, velocity and health
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.vel = vec(Zombie_acc, 0)
        self.health = 50

    #this function is for the horizontal collision
    def wallCollisions(self, platforms):
        #this for loop goes over all of the zombie barriers
        for wall in platforms:
            #this checks if the zombie is colliding with the zombie barriers
            if pygame.sprite.collide_rect(self, wall):
                #this checks if they are moving right, if they are it puts them to the left of the collision
                # and makes them move in the opposite direction
                if self.vel.x > 0:
                    self.rect.right = wall.rect.left
                    self.vel.x *= -1
                #if they are not moving right, then it puts them to the right of the collision
                # and makes them move in the opposite dirrection
                elif self.vel.x < 0:
                    self.rect.left = wall.rect.right
                    self.vel.x *= -1


    #this is the function that updates the zombie sprites
    def update(self):
        #This moves the player rect by one and checks if it is hitting a platform, then moves it back
        self.rect.y += 1
        hit_y = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1

        #this checks if the zombie is colliding with a platform
        if hit_y:
            # if the zombie is falling, it stops it and pushes the zombie to the top of the collision
            if self.vel.y > 0:
                self.vel.y = 0
                self.rect.bottom = hit_y[0].rect.top

        #This gives the zombies their gravity, horizontal collision, updates their position based on their velocity and
        #their rect based on their position
        self.vel.y = Zombie_grav
        self.wallCollisions(self.game.Zombie_bar)
        self.pos += self.vel
        self.rect.midbottom = self.pos

        #if the zombies health is zero it kills the zombie
        if self.health <= 0:
            self.kill()
    #this function draws the zombies health
    def draw_health(self):
        #based on their health the bar is a different colour
        if self.health > 40:
            col = Green
        elif self.health > 20:
            col = Yellow
        else:
            col = Red
        #the width of the zombie health bar depends on its health and is shown
        width = int(self.rect.width * self.health / 100)
        self.healh_bar = pygame.Rect(0, 0, width, 7)




#this is the platform class, it is initilized and it's hitbox is crated
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface((w, h))
                self.image.fill(Green)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y

#this is the zombie barrier class, it is initilized and it's hitbox is crated
class Zombie_bar(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
#this is the exit class, it is initilized and it's hitbox is crated
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#this is the coin class, it is initilized, it's hitbox is crated and it's image and rect are created
class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        #the coin is added to the all sprites group and coin group
        self.groups = game.all_sprites, game.coin
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.topleft = self.pos

#this is the spike class, it is initilized and it's hitbox is crated
class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Exit_final(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




