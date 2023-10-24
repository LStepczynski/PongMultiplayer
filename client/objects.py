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



class Ball(pg.Rect):
    def __init__(self, surface, position, size):
        self.surface = surface
        super().__init__(position[0], position[1], size[0], size[1])
    
    def draw(self):
        pg.draw.rect(self.surface, Colors.GRAY, self)

    def tick(self, direction):
        if direction == [True, True]:
            self.y -= gv.BALL_VELOCITY
            self.x += gv.BALL_VELOCITY
        if direction == [True, False]:
            self.y += gv.BALL_VELOCITY
            self.x += gv.BALL_VELOCITY
        if direction == [False, True]:
            self.y -= gv.BALL_VELOCITY
            self.x -= gv.BALL_VELOCITY
        if direction == [False, False]:
            self.y += gv.BALL_VELOCITY
            self.x -= gv.BALL_VELOCITY
