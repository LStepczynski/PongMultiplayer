from config import Game_properties as gp
import threading
import random
import json
import time


class Client:
    def __init__(self, server, game_room, address, player, enemy, ball) -> None:
        self.server = server
        self.game_room = game_room
        self.address = address
        self.player = player
        self.enemy = enemy
        self.ball = ball
        self.info = None

    def receive_info(self, info):
        try:
            self.info = json.loads(info.decode('utf-8'))
            print(self.info)
            self.update_player()
        except Exception as e:
            print(e)


    def update_player(self):
        if self.info == None:
            return
        for char in self.info:
            if char == '':
                continue
            if char == 'w':
                self.player[1] -= gp.VELOCITY
            if char == 's':
                self.player[1] += gp.VELOCITY


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


    def send_info(self):
        try:
            self.server.info_socket.sendto(json.dumps((self.player, self.enemy, self.ball)).encode("utf-8"), self.address)
        except Exception as e:
            self.connected = False
            self.server.run = False
            print(e, 2)


class Gameroom:
    def __init__(self, server, game_room):
        self.server = server
        self.game_room = game_room

        self.run = True

        self.client1 = Client(self.server,
                            self.game_room,
                            self.game_room[0],
                            [50, gp.HEIGHT // 2 - 100, 50, 200],
                            [gp.WIDTH - 100, gp.HEIGHT // 2 - 100, 50, 200],
                            [gp.WIDTH // 2 - 25, gp.HEIGHT // 2 - 25, 50, 50])

        self.client2 = Client(self.server,
                            self.game_room,
                            self.game_room[1],
                            [50, gp.HEIGHT // 2 - 100, 50, 200],
                            [gp.WIDTH - 100, gp.HEIGHT // 2 - 100, 50, 200],
                            [gp.WIDTH // 2 - 25, gp.HEIGHT // 2 - 25, 50, 50])
        
        self.direction = [bool(random.randint(0, 1)), bool(random.randint(0, 1))]

        threading.Thread(target=self.main_loop).start()


    def main_loop(self):
        while self.run:
            try:
                self.client1.update_ball(self.direction)
                self.client2.update_ball([not self.direction[0], self.direction[1]])

                self.exchange()

                self.client1.send_info()
                self.client2.send_info()

                self.client1.info = None
                self.client2.info = None
                time.sleep(1 / gp.TICK_RATE)
            except Exception as e:  # General exception to catch any error
                self.run = False
                print(f"An error occurred: {e}")
    

    def exchange(self):
        self.client1.enemy[1] = self.client2.player[1]
        self.client2.enemy[1] = self.client1.player[1]