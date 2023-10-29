from config import Game_properties as gp
from objects import *
import pygame as pg
import threading
import json


class Game:
    def __init__(self, client):
        pg.init()

        self.root = pg.display.set_mode((gp.WIDTH, gp.HEIGHT))
        pg.display.set_caption(gp.TITLE)

        self.stage = 0
        self.client = client
        self.score = [0, 0]

        self.player = Racket(self.root, (50, gp.HEIGHT//2-100), (50, 200))
        self.enemy = Racket(self.root, (gp.WIDTH-100, gp.HEIGHT//2-100), (50, 200))
        self.ball = Ball(self.root, (gp.WIDTH//2-25, gp.HEIGHT//2-25), (50, 50))

        threading.Thread(target=self.receive_positions).start()

        self.clock = pg.time.Clock()
        while self.client.run:
            self.clock.tick(gp.TICK_RATE)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.client.run = False
                    self.client.connection_socket.close()
                    return
            
            self.draw()
            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_SPACE] and self.stage == 0:
                self.client.connect()
                self.stage = 1

            self.user_input(keys_pressed)

            pg.display.update()
    

    def user_input(self, keys_pressed):
        if keys_pressed[pg.K_w]:
            self.client.info_socket.sendto(json.dumps('w').encode('utf-8'), self.client.info_addr)
            print('w')
        if keys_pressed[pg.K_s]:
            self.client.info_socket.sendto(json.dumps('s').encode('utf-8'), self.client.info_addr)
            print('s')


    def receive_positions(self):
        while self.client.run:
            try:
                data, addr = self.client.info_socket.recvfrom(1024)
                data = json.loads(data.decode('utf-8'))
                if data == "Connection Ended":
                    self.client.run = False

                self.score = data[3]
                self.player.set(data[0])
                self.enemy.set(data[1])
                self.ball.set(data[2])
            except Exception as e:
                print(e, 'aaa')


    def draw(self):
        self.root.fill(Colors.BLACK)
        match self.stage:
            case 0:
                self.root.blit(GameFonts.main_title, (gp.WIDTH//2 - GameFonts.main_title.get_width()//2,150))
                self.root.blit(GameFonts.author_title, (gp.WIDTH//2 - GameFonts.author_title.get_width()//2,300))
                self.root.blit(GameFonts.instruction_title, (gp.WIDTH//2 - GameFonts.instruction_title.get_width()//2,600))
            case 1:
                score = GameFonts.main_font_big.render(f"{self.score[0]} | {self.score[1]}", True, (255,255,255))
                print(f"{self.score[0]} | {self.score[1]}")
                self.root.blit(score, (gp.WIDTH//2 - score.get_width()//2,30))
                self.player.draw()
                self.enemy.draw()
                self.ball.draw()
