import socket
from threading import Thread
import tkinter
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
socket_open = True

def receive():
    global socket_open
    while socket_open:
        try:
            message = client_socket.recv(1024).decode()
            if message == "SHUTDOWN":
                print("The server has shut down!")
                client_socket.close()
                socket_open = False
                sys.exit()
            print(message)
        except socket.error:
            print("An error occurred!")
            client_socket.close()
            break

welcome_message = """
Welcome to the Chat Room!
Please enter your name to enter the server.
If you want to send a private message use "/msg" followed by the name and the message.

                    "/msg John Hello, how are you?"
                    
If you want to ban someone from texting in the chat room use "/ban" followed by the name.
You will need at least one more person to agree with your action. The user can still view
public conversations but is not able to type.

If you want to exit use the "/exit" command.
"""

print(welcome_message)

while True:
    username = input("Username: ")
    if username != "":
        client_socket.send(f"/username {username}".encode())
        break

receive_thread = Thread(target=receive)
receive_thread.start()

while client_socket:
    user_input = input()

    if user_input == "/exit":
        print("Exit the chat room")
        client_socket.send(user_input.encode())
        socket_open = False
        break
    
    client_socket.send(user_input.encode())

client_socket.close()
