from gameroom import Gameroom
import threading
import json
import socket
import time



class Server:
    def __init__(self):
        self.server_password = 'greensock'

        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_socket.bind(('0.0.0.0', 12345))

        self.info_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.info_socket.bind(('0.0.0.0', 12346))

        self.connected_clients = []
        self.game_rooms = []
        self.waiting = False
        self.run = True

        self.message_manager = threading.Thread(target=self.handle_messages)
        self.message_manager.start()

        threading.Thread(target=self.debug).start()

    
    def main(self):
        while self.run:
            self.connection_socket.listen()
            conn, _ = self.connection_socket.accept()
            addr, password = json.loads(conn.recv(1024).decode('utf-8'))
            
            if password != self.server_password:
                conn.close()
                continue

            addr = tuple(addr)

            if self.waiting:
                self.game_rooms[-1][1] = addr
                self.game_rooms[-1].append(Gameroom(self, self.game_rooms[-1]))
            else:
                self.game_rooms.append([addr, None])

            self.waiting = not self.waiting

            conn.settimeout(15)

            self.connected_clients.append(addr)

            threading.Thread(target=self.handle_connection, args=(conn, addr)).start()


    def handle_messages(self):
        while self.run:
            try:
                data, addr = self.info_socket.recvfrom(1024)
                
                if addr not in self.connected_clients:
                    continue

                for room in self.game_rooms:
                    if addr in room:
                        index = room.index(addr)
                        game_room = room
                if None in game_room:
                    continue

                if index == 0:
                    game_room[2].client1.receive_info(data)
                else:
                    game_room[2].client2.receive_info(data)
            except Exception as e:
                print(e)
                return


    def handle_connection(self, conn: socket.socket, addr):
        while self.run:
            try:
                data = conn.recv(1024)
                if not data:  # This checks for the empty bytes object signaling a closed connection
                    print('dc')
                    self.remove_client(addr)
                    return
                print('connection recv')
            except Exception as e:
                print(f'Exception: {e}')
                print('dc')
                self.remove_client(addr)
                return

            
    def remove_client(self, addr):
        for room in self.game_rooms:
            if addr not in room:
                continue
            self.game_rooms.remove(room)
            if None in room:
                self.waiting = False
                self.connected_clients.remove(addr)
            else:
                for i in (0,1):
                    self.info_socket.sendto(json.dumps('Connection Ended').encode('utf-8'), room[i])
                    self.connected_clients.remove(room[i])
                room[2].run = False




    
    def debug(self):
        """TEMPORARY FUNCTION"""
        while self.run:
            time.sleep(3)
            # print(self.connected_clients)
            print(self.game_rooms)
            print(self.waiting)
        

s = Server()
s.main()