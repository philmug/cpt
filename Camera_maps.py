import pygame
import pytmx
from Settings import *

class maps:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename)
        self.mapWidth = tm.width * tm.tilewidth
        self.mapHeight = tm.height * tm.tileheight
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
            temp_surface = pygame.Surface((self.mapWidth, self.mapHeight))
            self.render(temp_surface)
            return temp_surface

class camera:
    def __init__(self, cameraWidth, cameraHeight):
        self.camera = pygame.Rect(0, 0, cameraWidth, cameraHeight)
        self.cameraWidth = cameraWidth
        self.cameraHeight = cameraHeight

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        camera_x = -target.rect.x + int(Width/2)
        camera_y = -target.rect.y + int(Height/2)




        self.camera = pygame.Rect(camera_x, camera_y, self.cameraWidth, self.cameraHeight)


    def applyRect(self, rect):
        return rect.move(self.camera.topleft)