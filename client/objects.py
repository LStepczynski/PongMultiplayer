from config import Colors, Game_properties as gv
import pygame as pg


class GameFonts:
    pg.init()
    
    main_font_huge = pg.font.Font("Super Comic.ttf", 108)
    main_font_big = pg.font.Font("Super Comic.ttf", 52)
    main_font_small = pg.font.Font("Super Comic.ttf", 36)

    main_title = main_font_huge.render("PONG", True, (255, 255, 255))
    author_title = main_font_big.render("BY LSTEPCZYNSKI", True, (255,255,255))
    instruction_title = main_font_small.render("PRESS SPACE TO CONNECT TO THE SERVER", True, (255,255,255))


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
