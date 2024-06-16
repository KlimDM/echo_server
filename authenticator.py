import os
import hashlib
import socket
import uuid


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8880))
server_socket.listen(5)

users = {}

if os.path.isfile('users.txt'):
    with open('users.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(',')
            users[username] = {'password': password, 'token': None}

while True:
    try:
        client_socket, client_address = server_socket.accept()
        ip = client_address[0]

        message = client_socket.recv(1024).decode()

        if message.startswith('REGISTER'):
            username, password = message.split(' ')[1:]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            token = str(uuid.uuid4())
            users[username] = {'password': hashed_password, 'token': token}
            with open('users.txt', 'a') as f:
                f.write(f'{username},{hashed_password}\n')
            client_socket.send(token.encode())
        elif message.startswith('LOGIN'):
            username, password = message.split(' ')[1:]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if username in users and users[username]['password'] == hashed_password:
                token = str(uuid.uuid4())
                users[username]['token'] = token
                client_socket.send(token.encode())
            else:
                client_socket.send('Неверные учетные данные'.encode())
        elif message.startswith('CHECK_TOKEN'):
            token = message.split(' ')[1]
            if token in [user['token'] for user in users.values()]:
                client_socket.send('OK'.encode())
            else:
                client_socket.send('Неверный токен'.encode())

    except (ConnectionResetError, BrokenPipeError):
        pass

    server_socket.close()