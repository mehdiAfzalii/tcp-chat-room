import threading
import socket

HOST = 'localhost'
PORT = 9998

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()

        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print(f"{nickname} joined the chat! 😀")
        client.send('connected to server!'.encode('utf-8'))

        th = threading.Thread(target=handle, args=(client,))
        th.start()


print('SERVER IS LISTENING...')
receive()
