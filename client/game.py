from config import Game_properties as gp
from objects import *
import pygame as pg
import threading
import json


class Game:
    def __init__(self, client):
        self.root = pg.display.set_mode((gp.WIDTH, gp.HEIGHT))
        pg.display.set_caption(gp.TITLE)

        self.client = client
        self.once = True

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
            if keys_pressed[pg.K_SPACE] and self.once:
                self.client.connect()
                self.once = False

            self.user_input(keys_pressed)

            pg.display.update()
    

    def user_input(self, keys_pressed):
        if keys_pressed[pg.K_w]:
            self.client.info_socket.sendto(json.dumps('w').encode('utf-8'), self.client.info_addr)
        if keys_pressed[pg.K_s]:
            self.client.info_socket.sendto(json.dumps('s').encode('utf-8'), self.client.info_addr)


    def receive_positions(self):
        while self.client.run:
            try:
                data, addr = self.client.info_socket.recvfrom(1024)
                data = json.loads(data.decode('utf-8'))
                if data == "Connection Ended":
                    self.client.run = False

                self.player.set(data[0])
                self.enemy.set(data[1])
                self.ball.set(data[2])
            except Exception as e:
                print(e)


    def draw(self):
        self.root.fill(Colors.BLACK)
        self.player.draw()
        self.enemy.draw()
        self.ball.draw()
