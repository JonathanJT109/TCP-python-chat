import socket
from threading import Thread
import sys
import random
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
server_socket.listen()


def send_all(message):
    for client in clients:
        client.send(message.encode())

def send_to(message, sender):
    message_to_send = f"{clients[sender].color}{clients[sender].name}: {message}{Fore.RESET}"
    print(message_to_send)
    for client in clients:
        if client != sender:
            client.send(message_to_send.encode())


def messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "/exit":
                print(f"{clients[client].name} left the server")
                client.close()
                del clients[client]
                break
            elif message.startswith("/username"):
                clients[client].name = message.split()[1]
            else:
                send_to(message, client)
        except socket.error:
            if client in clients:
                client.close()
                del clients[client]
            break


def server_commands():
    deleted_clients = []

    while True:
        command = input()

        if command == "/exit":
            print("Exit the server")

            for client in clients:
                client.send("SHUTDOWN".encode())
                deleted_clients.append(client)

            for client in deleted_clients:
                del clients[client]

            server_socket.close()
            sys.exit()

        elif command == "/number":
            print("Number of clients:", len(clients))


def main():
    while True:
        client, address = server_socket.accept()

        if client not in clients:
            client_color = random.choice(colors)
            clients[client] = User("", datetime.now(), 0, "active", client_color)

        print("Connection from", address, "has been established!")

        thread = Thread(target=messages, args=(client,))
        thread.start()


if __name__ == "__main__":
    print("Server is listening...")
    thread = Thread(target=server_commands)
    thread.start()
    main()
