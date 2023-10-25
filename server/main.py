from config import Game_properties as gp
from game_room import Game_room
import socket as sk
import threading
import pickle
import random
import time


class Server:
    def __init__(self, server_socket, server_address):
        self.server_socket = server_socket
        self.server_address = server_address

        self.connected_clients = []
        self.game_rooms = []
        self.waiting = False

        self.server_socket.bind(self.server_address)

        self.server_socket.listen(2)
        print("Server is listening for connections...")

        self.run = True
        while self.run:
            print(self.connected_clients)
            print(self.game_rooms)
            # Wait for a client to connect
            client_socket, client_address = self.server_socket.accept()

            # Handles creating and joining game rooms
            if self.waiting:
                self.game_rooms[-1][1] = (client_socket, client_address)
                threading.Thread(target=self.handle_game, args=(self.game_rooms[-1],)).start()
            else:
                self.game_rooms.append([(client_socket, client_address), None])
            
            self.waiting = not self.waiting

            # Appends the client to the connected clients
            self.connected_clients.append((client_socket, client_address))

    def handle_game(self, game_room):
        Game_room(game_room)



    def handle_client(self, socket, address, event):
        print(f"Connection from {address} established.")
        
        try:
            while not event.is_set():
                response = pickle.loads(socket.recv(1024))
                for client_socket, client_address in self.connected_clients:
                    if (client_socket, client_address) != (socket, address):
                        client_socket.send(pickle.dumps("enemy:"+response))
                if not response:
                    break  # No more data from the client, exit the loop
                print(response)
        except ConnectionResetError:
            pass  # Handle the case where the client abruptly disconnects
        print('DEL')
        event.set()
        self.connected_clients.remove((socket, address))
        socket.close()


Server(sk.socket(sk.AF_INET, sk.SOCK_STREAM), ('0.0.0.0', 12345))
