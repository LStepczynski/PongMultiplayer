import threading
import json
import socket
import time

class Server:
    def __init__(self):
        self.server_password = 'greensock'

        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_socket.bind(('localhost', 12345))

        self.info_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.info_socket.bind(('localhost', 12346))

        self.connected_clients = []
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

            conn.settimeout(15)

            self.connected_clients.append(addr)

            threading.Thread(target=self.handle_connection, args=(conn, addr)).start()


    def handle_messages(self):
        while self.run:
            try:
                data, addr = self.info_socket.recvfrom(1024)
                
                if addr not in self.connected_clients:
                    continue

                print(f"{addr} : {json.loads(data.decode('utf-8'))}")
                
            except Exception as e:
                print(e)
                return


    def handle_connection(self, conn: socket.socket, addr):
        while self.run:
            try:
                data = conn.recv(1024)
                if not data:  # This checks for the empty bytes object signaling a closed connection
                    print('dc')
                    self.connected_clients.remove(addr)
                    return
                print('connection recv')
            except Exception as e:
                print(f'Exception: {e}')
                print('dc')
                self.connected_clients.remove(addr)
                return

            
    
    def debug(self):
        """TEMPORARY FUNCTION"""
        while self.run:
            time.sleep(3)
            print(self.connected_clients)
        

s = Server()
s.main()