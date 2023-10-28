from config import Game_properties as gp
import threading
import pickle
import random
import time


class Client:
    def __init__(self, game_room, address, player, enemy, ball) -> None:
        self.game_room = game_room
        self.address = address
        self.player = player
        self.enemy = enemy
        self.ball = ball
        self.info = None
    
    def receive_info(self, info):
        """Receive input from the client"""
        try:
            self.info = pickle.loads(info)
            self.update_player()

        except Exception as e:
            print(e, 1)

    def send_info(self):
        """Send info to the client"""
        try:
            # Positions of the rackets and the ball
            self.game_room.server_socket.sendto(pickle.dumps((self.player, self.enemy, self.ball)), self.address)

        except Exception as e:
            self.game_room.run = False
            print(e, 2)


    def update_ball(self, direction):
        """Handles the movement of the ball"""

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
                self.player[1] -= gp.VELOCITY
            if char == 's':
                self.player[1] += gp.VELOCITY


        

class Game_room:
    def __init__(self, game_room, server_socket):
        self.run = True  

        self.game_room = game_room
        self.server_socket = server_socket

        # Create the client objects
        self.client1 = Client(self,
                              game_room[0],  # Client address
                              [50, gp.HEIGHT // 2 - 100, 50, 200],
                              [gp.WIDTH - 100, gp.HEIGHT // 2 - 100, 50, 200],
                              [gp.WIDTH // 2 - 25, gp.HEIGHT // 2 - 25, 50, 50])

        self.client2 = Client(self,
                              game_room[1],  # Client address
                              [50, gp.HEIGHT // 2 - 100, 50, 200],
                              [gp.WIDTH - 100, gp.HEIGHT // 2 - 100, 50, 200],
                              [gp.WIDTH // 2 - 25, gp.HEIGHT // 2 - 25, 50, 50])

        # Decide the initial direction of the ball
        self.direction = [bool(random.randint(0, 1)), bool(random.randint(0, 1))]

        # Start the main loop 
        self.loop_thread = threading.Thread(target=self.main_loop)
        self.loop_thread.start()

    def main_loop(self):
        """Main loop of the program"""
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

