import socket
import threading
import tkinter

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

welcome_message = """
Welcome to the Chat Room!
Please enter your name and a message to enter.
If you want to send a private message use "/msg" followed by the name and the message.

                    "/msg John Hello, how are you?"
                    
If you want to ban someone from texting in the chat room use "/ban" followed by the name.
You will need at least one more person to agree with your action. The user can still view
public conversations but is not able to type.

If you want to exit use the "/exit" command.
"""

print(welcome_message)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

message = client_socket.recv(1024).decode()

while message:
    if message == "/exit":
        print("Exit the sever")
        break
    print("Message:", message)
    message = client_socket.recv(1024).decode()

client_socket.close()
