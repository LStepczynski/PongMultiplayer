from config import Game_properties as gp
import threading
import random
import json
import time


class Client:
    def __init__(self, client, server, address, player, enemy, ball, main = False) -> None:
        self.client = client
        self.server = server
        self.address = address
        self.player = player
        self.enemy = enemy
        self.ball = ball
        self.main = main
        self.info = None

    def receive_info(self, info):
        try:
            self.info = json.loads(info.decode('utf-8'))
            if not self.client.wait:
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


    def update_ball(self, direction, x_ball_vel, y_ball_vel):
        for _ in range(5):
            if direction == [True, True]:
                self.ball[1] -= y_ball_vel/5
                self.ball[0] += x_ball_vel/5
            if direction == [True, False]:
                self.ball[1] += y_ball_vel/5
                self.ball[0] += x_ball_vel/5
            if direction == [False, True]:
                self.ball[1] -= y_ball_vel/5
                self.ball[0] -= x_ball_vel/5
            if direction == [False, False]:
                self.ball[1] += y_ball_vel/5
                self.ball[0] -= x_ball_vel/5

            # is main client | chceks if ball's x is smaller than zero 
            if self.main and self.ball[0] - x_ball_vel + 5 <= 0:
                self.client.score[1] += 1
                self.client.start()
                return
            
            # is main client | chceks if ball's x + ball velocity is bigger than the width of the screen 
            if self.main and self.ball[0] + x_ball_vel + self.ball[2] - 5 >= gp.WIDTH:
                self.client.score[0] += 1
                self.client.start()
                return

            # Checks if ball's x - ball's vel is smaller than player's x | checks if the ball is in front of the player
            if self.ball[0] - x_ball_vel + 5 <= self.player[0] + self.player[2] and (self.ball[1] + self.ball[3] > self.player[1] and self.ball[1] < self.player[1] + self.player[3]):
                self.client.change_ball_velocity()
                direction[0] = True

            # Checks if ball's x + ball's vel + ball's width is larger than player's x | checks if the ball is in front of the enemy
            if self.ball[0] + x_ball_vel + self.ball[2] - 5 >= self.enemy[0] and (self.ball[1] + self.ball[3] > self.enemy[1] and self.ball[1] < self.enemy[1] + self.enemy[3]):
                self.client.change_ball_velocity()
                direction[0] = False

            # Checks if 
            if self.ball[1] - y_ball_vel + 5 <= 0:
                self.client.change_ball_velocity()
                direction[1] = False
            if self.ball[1] + y_ball_vel + self.ball[3] - 5 >= gp.HEIGHT:
                self.client.change_ball_velocity()
                direction[1] = True


    def send_info(self):
        try:
            score = self.client.score if self.main else [self.client.score[1], self.client.score[0]]
            data = json.dumps((self.player, self.enemy, self.ball, score)).encode("utf-8")
            self.server.info_socket.sendto(data, self.address)
        except Exception as e:
            self.connected = False
            self.server.run = False
            print(e, 2)


class Gameroom:
    def __init__(self, server, game_room):
        self.server = server
        self.game_room = game_room

        self.wait = False
        self.run = True

        self.score = [0, 0]

        self.start()

        self.wait = False
        time.sleep(3)

        threading.Thread(target=self.main_loop).start()


    def start(self):
        self.client1 = Client(self,
                            self.server,
                            self.game_room[0],
                            [50, gp.HEIGHT // 2 - 100, 50, 200],
                            [gp.WIDTH - 100, gp.HEIGHT // 2 - 100, 50, 200],
                            [gp.WIDTH // 2 - 25, gp.HEIGHT // 2 - 25, 50, 50],
                            True)

        self.client2 = Client(self,
                            self.server,
                            self.game_room[1],
                            [50, gp.HEIGHT // 2 - 100, 50, 200],
                            [gp.WIDTH - 100, gp.HEIGHT // 2 - 100, 50, 200],
                            [gp.WIDTH // 2 - 25, gp.HEIGHT // 2 - 25, 50, 50])
        
        self.direction = [bool(random.randint(0, 1)), bool(random.randint(0, 1))]
        self.x_ball_vel = gp.MIN_BALL_VELOCITY//2
        self.y_ball_vel = gp.MIN_BALL_VELOCITY//2

        self.wait = True
        


    def main_loop(self):
        while self.run:
            try:
                self.client1.update_ball(self.direction, self.x_ball_vel, self.y_ball_vel)
                self.client2.update_ball([not self.direction[0], self.direction[1]], self.x_ball_vel, self.y_ball_vel)

                self.exchange()

                self.client1.send_info()
                self.client2.send_info()

                self.client1.info = None
                self.client2.info = None
                time.sleep(1 / gp.TICK_RATE)
                if self.wait:
                    time.sleep(3)
                    self.wait = False
            except Exception as e:  # General exception to catch any error
                self.run = False
                print(f"An error occurred: {e}")


    def change_ball_velocity(self):
        self.x_ball_vel = random.randint(gp.MIN_BALL_VELOCITY, gp.MAX_BALL_VELOCITY)
        self.y_ball_vel = random.randint(gp.MIN_BALL_VELOCITY, gp.MAX_BALL_VELOCITY)


    def exchange(self):
        self.client1.enemy[1] = self.client2.player[1]
        self.client2.enemy[1] = self.client1.player[1]