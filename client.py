import socket

DEFAULT_SERVER_PORT = 9090
IDENTIFIER_PORT = 1234
AUTH_PORT = 8880

DEFAULT_HOST = "localhost"
IDENTIFIER_FIRST_MESSAGE = "Введите ваше имя: "

sock = socket.socket()
sock.setblocking(True)


def connect_to_server():
    try:
        host = input("Введите адрес сервера: ")
        port = int(input("Введите порт: "))
        sock.connect((host, port))
    except Exception:
        sock.connect((DEFAULT_HOST, DEFAULT_SERVER_PORT))

    while True:
        msg = input("Введите сообщение: ")
        if msg == "break":
            break
        sock.send(msg.encode())
        data = sock.recv(1024)
        sock.settimeout(None)
        print(data.decode())
    sock.close()


def connect_to_identifier():
    try:
        sock.connect((DEFAULT_HOST, IDENTIFIER_PORT))
    except Exception:
        print("Ошибка подключения к серверу аутентификации")
    message = sock.recv(1024).decode()
    print(message)
    if message == IDENTIFIER_FIRST_MESSAGE:
        name = input()
        sock.send(name.encode())
    message = sock.recv(1024).decode()
    print(message)
    sock.close()


def connect_to_auth():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(('localhost', AUTH_PORT))

    try:
        username = input('Введите имя пользователя: ')
        password = input('Введите пароль: ')
        message = f'REGISTER {username} {password}'
        client_socket.send(message.encode())

        token = client_socket.recv(1024).decode()

        message = f'LOGIN {username} {password}'
        client_socket.send(message.encode())

        response = client_socket.recv(1024).decode()
        print(response)
        client_socket.close()
    except Exception:
        print("ошибка на сервере аутентификации")



if __name__ == "__main__":
    connect_to_server()
    # connect_to_identifier()
    # connect_to_auth()