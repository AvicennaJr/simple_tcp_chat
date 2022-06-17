import socket
import threading

host = "127.0.0.1"
port = 65000

nickname = input("Choose a nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

#Defined two functions that will run simultaneously
#one for sending messages, the next to receive messages

def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == 'NICK':
                client.send(nickname.encode("ascii"))
            else:
                print(message)
        except:
            print("An error occured")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

 
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
