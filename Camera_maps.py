#these are importing pygame, pytmx and everything from the settings file
import pygame
import pytmx
from Settings import *

#this is the maps class
class maps:
    #initiating the map class and getting the data from the map file
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename)
        self.map_width = tm.width * tm.tilewidth
        self.map_height = tm.height * tm.tileheight
        self.tmxdata = tm

    #This function renders the map files into images
    def render(self, surface):
        #this gets the time image information
        ti = self.tmxdata.get_tile_image_by_gid
        #this for loop goes over every visible layer in the map file
        for layer in self.tmxdata.visible_layers:
            #This if statement checks if the layer is a tmx tiled tile layer
            if isinstance(layer, pytmx.TiledTileLayer):
                #this for loop goes over every block on the layer
                for x, y, gid in layer:
                    #the tile variable is assaigned the value of the x, y and type of the block
                    tile = ti(gid)
                    #this if statement is checking if there is a tile and if there is then it blit's it on the surface
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    #this function puts the rendered map image on a temporary surface and returns the temporary surface
    def Make_map(self):
            temp_surface = pygame.Surface((self.map_width, self.map_height))
            self.render(temp_surface)
            return temp_surface

#this is the camera class
class camera:
    #this initiates the class and the valriables used in the class
    def __init__(self, camera_width, camera_height):
        self.camera = pygame.Rect(0, 0, camera_width, camera_height)
        self.camera_width = camera_width
        self.camera_height = camera_height

    #this function checks where the entities need to be on the screen
    def apply(self, entity):
        # it returns how much the entities need to move by which is the value of how much the camera mouved
        return entity.rect.move(self.camera.topleft)

    #this function moves the camera rect to keep the player in the center of the screen
    def update(self, target):
        camera_x = -target.rect.x + int(Width/2)
        camera_y = -target.rect.y + int(Height/2)

        #thse if statements check if the camera rect if off the level and then repositions it to only show the level
        if camera_x >= 0:
            camera_x = 0
        if camera_y >= 0:
            camera_y = 0

        #this is updating the camera values
        self.camera = pygame.Rect(camera_x, camera_y, self.camera_width, self.camera_height)

    #This moves the camera to the camera rect
    def applyRect(self, rect):
        return rect.move(self.camera.topleft)




