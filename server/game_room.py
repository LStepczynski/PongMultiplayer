from config import Game_properties as gp
import threading
import pickle
import random
import time


class Client:
    def __init__(self, socket, address, player, enemy, ball) -> None:
        self.socket = socket
        self.address = address
        self.player = player
        self.enemy = enemy
        self.ball = ball
        self.info = None
        self.connected = True
    
    def receieve_info(self):
        while self.connected:
            self.info = pickle.loads(self.socket.recv(1024))
            print(self.info)
            self.update_player()
    
    def send_info(self):
        self.socket.send(pickle.dumps((self.player, self.enemy, self.ball)))
        
    def update(self, direction):
        self.update_ball(direction)
        self.update_player()
    
    def update_ball(self, direction):
        for _ in range(10):
            if direction == [True, True]:
                self.ball[1] -= gp.BALL_VELOCITY/10
                self.ball[0] += gp.BALL_VELOCITY/10
            if direction == [True, False]:
                self.ball[1] += gp.BALL_VELOCITY/10
                self.ball[0] += gp.BALL_VELOCITY/10
            if direction == [False, True]:
                self.ball[1] -= gp.BALL_VELOCITY/10
                self.ball[0] -= gp.BALL_VELOCITY/10
            if direction == [False, False]:
                self.ball[1] += gp.BALL_VELOCITY/10
                self.ball[0] -= gp.BALL_VELOCITY/10

            if self.ball[0] - gp.BALL_VELOCITY + 5 <= 0:
                direction[0] = True
            if self.ball[0] + gp.BALL_VELOCITY + self.ball[2] - 5 >= gp.WIDTH:
                direction[0] = False

            if self.ball[0] - gp.BALL_VELOCITY + 5 <= self.player[0] + self.player[2] and (self.ball[1] > self.player[1] and self.ball[1] < self.player[1] + self.player[3]):
                direction[0] = True
            if self.ball[0] + gp.BALL_VELOCITY + self.ball[2] - 5 >= self.enemy[0] and (self.ball[1] > self.enemy[1] and self.ball[1] < self.enemy[1] + self.enemy[3]):
                direction[0] = False

            if self.ball[1] - gp.BALL_VELOCITY + 5 <= 0:
                direction[1] = False
            if self.ball[1] + gp.BALL_VELOCITY + self.ball[3] - 5 >= gp.HEIGHT:
                direction[1] = True

    def update_player(self):
        if self.info == None:
            return
        for char in self.info:
            if char == '':
                continue
            if char == 'w':
                print('a')
                self.player[1] -= gp.VELOCITY
            if char == 's':
                print('b')
                self.player[1] += gp.VELOCITY

    def disconect(self):
        self.socket.close()
        self.connected = False

        


class Game_room:
    def __init__(self, game_room):
        self.client1 = Client(game_room[0][0], 
                              game_room[0][1],
                              [50, gp.HEIGHT//2-100, 50, 200],
                              [gp.WIDTH-100, gp.HEIGHT//2-100, 50, 200],
                              [gp.WIDTH//2-25, gp.HEIGHT//2-25, 50, 50])
    
        self.client2 = Client(game_room[1][0], 
                              game_room[1][1],
                              [50, gp.HEIGHT//2-100, 50, 200],
                              [gp.WIDTH-100, gp.HEIGHT//2-100, 50, 200],
                              [gp.WIDTH//2-25, gp.HEIGHT//2-25, 50, 50])

        self.direction = [bool(random.randint(0, 1)), bool(random.randint(0, 1))]

        self.client1_thread = threading.Thread(target=self.client1.receieve_info)
        self.client1_thread.start()

        self.client2_thread = threading.Thread(target=self.client2.receieve_info)
        self.client2_thread.start()

        while True:
            try:
                self.client1.update_ball(self.direction)
                self.client2.update_ball([not self.direction[0], self.direction[1]])

                self.exchange()

                self.client1.send_info()
                self.client2.send_info()

                self.client1.info = None
                self.client2.info = None
                time.sleep(1/gp.TICK_RATE)
            except ConnectionResetError:
                self.client1.disconect()
                self.client2.disconect()
                break

    def exchange(self):
        self.client1.enemy[1] = self.client2.player[1]
        self.client2.enemy[1] = self.client1.player[1]

