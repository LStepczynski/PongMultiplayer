from config import Colors, Game_properties as gp
from objects import Racket
import pygame as pg
import socket


class Game:
    def __init__(self, server_address, name) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.name = name

        self.root = pg.display.set_mode((gp.WIDTH, gp.HEIGHT))
        pg.display.set_caption(gp.TITLE)

        self.client_socket.connect(server_address)
        welcome_message = self.client_socket.recv(1024)
        print(welcome_message.decode())

        message = "Hello, server!"
        self.client_socket.send(message.encode())

        self.player = Racket(self.root, (50, 50), (50, 100))


        self.clock = pg.time.Clock()
        self.run = True
        while self.run:
            self.clock.tick(gp.TICK_RATE)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                    self.client_socket.send("siemano".encode())
                    self.client_socket.close()

            keys_pressed = pg.key.get_pressed()
    
            self.send_commands(keys_pressed)
            self.draw()
            self.tick(keys_pressed)

            pg.display.update()
            

    def draw(self):
        self.root.fill(Colors.BLACK)
        self.player.draw()

    def tick(self, keys_pressed):
        if keys_pressed[pg.K_w]:
            self.player.tick('up')
        elif keys_pressed[pg.K_s]:
            self.player.tick('down')

    def send_commands(self, keys_pressed):
        if keys_pressed[pg.K_w]:
            self.client_socket.send('w'.encode())
        if keys_pressed[pg.K_s]:
            self.client_socket.send('s'.encode())

Game(('localhost', 12345), input("name: "))