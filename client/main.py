from config import Colors, Game_properties as gp
from objects import Racket, Ball
import threading
import pygame as pg
import pickle
import socket
import time


class Game:
    def __init__(self, server_input_address, server_init_address, name) -> None:

        # Init the game window
        self.root = pg.display.set_mode((gp.WIDTH, gp.HEIGHT))
        pg.display.set_caption(gp.TITLE)

        self.run = True

        # Server addresses
        self.server_input_address = server_input_address
        self.server_init_address = server_init_address

        # Create the sockets        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.sendto(pickle.dumps(''), self.server_input_address)

        self.client_init_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_init_socket.connect(self.server_init_address)
        
        print('con')
        # Name of the client
        self.name = name

        # Create the objects of the game
        self.player = Racket(self.root, (50, gp.HEIGHT//2-100), (50, 200))
        self.enemy = Racket(self.root, (gp.WIDTH-100, gp.HEIGHT//2-100), (50, 200))
        self.ball = Ball(self.root, (gp.WIDTH//2-25, gp.HEIGHT//2-25), (50, 50))

        # Start the thread that will recieve information from the server
        threading.Thread(target=self.receive_commads).start()
        threading.Thread(target=self.pulse).start()
    
        # Main loop of the game
        self.clock = pg.time.Clock()
        while self.run:
            self.clock.tick(gp.TICK_RATE)

            # Event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                    self.client_socket.close()

            keys_pressed = pg.key.get_pressed()

            self.send_commands(keys_pressed)
            self.draw()


            pg.display.update()
    

    def pulse(self):
        while self.run:
            print('a')
            self.client_init_socket.send(pickle.dumps(""))
            time.sleep(5)


    def draw(self):
        """Draw all the objects on the screen"""
        self.root.fill(Colors.BLACK)
        self.player.draw()
        self.enemy.draw()
        self.ball.draw()

    def send_commands(self, keys_pressed):
        """Send user input to the server"""
        try:
            if keys_pressed[pg.K_w]:
                self.client_socket.sendto(pickle.dumps('w'), self.server_input_address)

            if keys_pressed[pg.K_s]:
                self.client_socket.sendto(pickle.dumps('s'), self.server_input_address)

        except Exception as e:
            self.run = False
            self.client_socket.close()
            print(e)
        
    def receive_commads(self):
        """Listen for messages from the server"""
        while self.run:
            try:
                # Receieve the tuple with positions of the objects
                info = self.client_socket.recv(1024)
                info = pickle.loads(info)

                # Set the positions of the objects to the ones received from the server
                self.player.set(info[0])
                self.enemy.set(info[1])
                self.ball.set(info[2])

            except Exception as e:
                print(e, 'aaaaaaaa')
                self.run = False
                self.client_socket.close()
                print(e)

Game(('localhost', 12345), ('localhost', 12346), input("name: "))