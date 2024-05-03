import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen(5)

clients = {}

if os.path.isfile('clients.txt'):
    with open('clients.txt', 'r') as f:
        for line in f:
            ip, name = line.strip().split(',')
            clients[ip] = name

while True:
    client_socket, client_address = server_socket.accept()
    ip = client_address[0]
    if ip in clients:
        client_socket.send(f'Привет, {clients[ip]}!'.encode())
    else:
        client_socket.send('Введите ваше имя: '.encode())
        name = client_socket.recv(1024).decode()
        clients[ip] = name
        with open('clients.txt', 'a') as f:
            f.write(f'{ip},{name}\n')
        client_socket.send(f'Привет, {name}!'.encode())

    client_socket.close()
