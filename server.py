import socket
import threading
from datetime import datetime
from colorama import Fore, init, Back


class User:
    def __init__(self, name, active_time, ban_counter, status, color):
        self.user_name = ""
        self.password = ""
        self.name = name
        self.active_time = active_time
        self.color = color
        self.status = status
        self.ban_counter = ban_counter


init()

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555
clients = {}
colors = [
    Fore.BLUE,
    Fore.CYAN,
    Fore.GREEN,
    Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTCYAN_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTYELLOW_EX,
    Fore.MAGENTA,
    Fore.YELLOW,
]


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)
print("Server is running and listening on port:", SERVER_PORT)
connection, address = server_socket.accept()
print(address, "has joined.")

message = "/exit"
connection.send(message.encode())

connection.close()
server_socket.close()
