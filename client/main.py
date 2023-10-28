from config import Colors, Game_properties as gp
from objects import Racket, Ball
import threading
import pygame as pg
import pickle
import socket


class Game:
    def __init__(self, server_address, name) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = server_address
        self.name = name

        self.root = pg.display.set_mode((gp.WIDTH, gp.HEIGHT))
        pg.display.set_caption(gp.TITLE)

        self.client_socket.sendto("".encode(), (server_address[0], server_address[1]+1))

        self.player = Racket(self.root, (50, gp.HEIGHT//2-100), (50, 200))
        self.enemy = Racket(self.root, (gp.WIDTH-100, gp.HEIGHT//2-100), (50, 200))
        self.ball = Ball(self.root, (gp.WIDTH//2-25, gp.HEIGHT//2-25), (50, 50))

        self.clock = pg.time.Clock()
        self.run = True
        threading.Thread(target=self.recieve_commads).start()
        while self.run:
            self.clock.tick(gp.TICK_RATE)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                    self.client_socket.close()

            keys_pressed = pg.key.get_pressed()

            self.send_commands(keys_pressed)
            self.draw()


            pg.display.update()
            

    def draw(self):
        self.root.fill(Colors.BLACK)
        self.player.draw()
        self.enemy.draw()
        self.ball.draw()

    def send_commands(self, keys_pressed):
        try:
            if keys_pressed[pg.K_w]:
                print('w')
                self.client_socket.sendto(pickle.dumps('w'), self.server_address)
            if keys_pressed[pg.K_s]:
                print('a')
                self.client_socket.sendto(pickle.dumps('s'), self.server_address)
        except Exception as e:
            self.run = False
            self.client_socket.close()
            print(e)
        
    def recieve_commads(self):
        while self.run:
            try:
                info = pickle.loads(self.client_socket.recv(1024))
                self.player.set(info[0])
                self.enemy.set(info[1])
                self.ball.set(info[2])
            except Exception as e:
                self.run = False
                self.client_socket.close()
                print(e)

Game(('25.55.142.184', 12345), input("name: "))