from config import Colors, Game_properties as gv
import pygame as pg


class Racket(pg.Rect):
    def __init__(self, surface, position, size):
        self.surface = surface
        super().__init__(position[0], position[1], size[0], size[1])

    def draw(self):
        pg.draw.rect(self.surface, Colors.WHITE, self)

    def tick(self, direction):
        if direction == 'up':
            self.y -= gv.VELOCITY
        elif direction == 'down':
            self.y += gv.VELOCITY
