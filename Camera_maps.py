import pygame
import pytmx
from Settings import *


class maps:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename)
        self.map_width = tm.width * tm.tilewidth
        self.map_height = tm.height * tm.tileheight
        self.tmxdata = tm


    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def Make_map(self):
            temp_surface = pygame.Surface((self.map_width, self.map_height))
            self.render(temp_surface)
            return temp_surface

class camera:
    def __init__(self, camera_width, camera_height):
        self.camera = pygame.Rect(0, 0, camera_width, camera_height)
        self.camera_width = camera_width
        self.camera_height = camera_height


    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        camera_x = -target.rect.x + int(Width/2)
        camera_y = -target.rect.y + int(Height/2)

        if camera_x >= 0:
            camera_x = 0
        if camera_y >= 0:
            camera_y = 0
        # if camera_x <= map1_length - self.camera_width:
        #     camera_x = map1_length - self.camera_width
        # if camera_y <= map1_height - self.camera_height:
        #     camera_y = map1_height - self.camera_height

        self.camera = pygame.Rect(camera_x, camera_y, self.camera_width, self.camera_height)


    def applyRect(self, rect):
        return rect.move(self.camera.topleft)