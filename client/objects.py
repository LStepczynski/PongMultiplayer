from config import Colors, Game_properties as gv
import pygame as pg


class Racket(pg.Rect):
    def __init__(self, surface, position, size):
        self.surface = surface
        super().__init__(position[0], position[1], size[0], size[1])

    def draw(self):
        pg.draw.rect(self.surface, Colors.WHITE, self)

    def set(self, position):
        self.x = position[0]
        self.y = position[1]



class Ball(pg.Rect):
    def __init__(self, surface, position, size):
        self.surface = surface
        super().__init__(position[0], position[1], size[0], size[1])
    
    def draw(self):
        pg.draw.rect(self.surface, Colors.GRAY, self)

    def set(self, position):
        self.x = position[0]
        self.y = position[1]
        self.width = position[2]
        self. height = position[3]
