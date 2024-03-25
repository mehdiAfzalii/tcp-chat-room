import threading
import socket

nickname = input("Choose a nickname : ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9998))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print('An error occurred!!!')
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))


re_th = threading.Thread(target=receive)
re_th.start()

wr_th = threading.Thread(target=write)
wr_th.start()
