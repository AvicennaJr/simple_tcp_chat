import threading
import socket

host = "127.0.0.1"
port = 65000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen()

clients = []
nicknames = []

def broadcast(message): #Send messages to all clients
    for client in clients:
        client.send(message)

def handle(client): #Handle messages from individual clients
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames(index)
            broadcast(f"{nickname} left the chat!".encode()('ascii'))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        #Use threading to manage multiple clients at once

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server is listening')
recieve()