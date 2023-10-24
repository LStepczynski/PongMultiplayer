from config import Colors, Game_properties as gp
from objects import Racket, Ball
import threading
import pygame as pg
import pickle
import socket


class Game:
    def __init__(self, server_address, name) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address
        self.name = name

        self.root = pg.display.set_mode((gp.WIDTH, gp.HEIGHT))
        pg.display.set_caption(gp.TITLE)

        self.client_socket.connect(server_address)

        self.ball_direction = pickle.loads(self.client_socket.recv(1024))
        print(self.ball_direction)

        message = "Hello, server!"
        self.client_socket.send(message.encode())

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
        self.enemy.draw()
        self.ball.draw()

    def tick(self, keys_pressed):
        if keys_pressed[pg.K_w]:
            self.player.tick('up')
        elif keys_pressed[pg.K_s]:
            self.player.tick('down')
        self.ball.tick(self.ball_direction)

    def send_commands(self, keys_pressed):
        if keys_pressed[pg.K_w]:
            self.client_socket.send('w'.encode())
        if keys_pressed[pg.K_s]:
            self.client_socket.send('s'.encode())
        
    def recieve_commads(self):
        while self.run:
            message = self.client_socket.recv(1024).decode()
            if message.startswith('enemy:'):
                message.replace("enemy:", "")
                for letter in message:
                    if letter == 'w':
                        self.enemy.tick('up')
                    elif letter == 's':
                        self.enemy.tick('down')

Game(('localhost', 12345), input("name: "))