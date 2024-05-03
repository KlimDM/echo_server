import socket

DEFAULT_PORT = 9090
DEFAULT_HOST = "localhost"
AUTH_HOST = "localhost"
AUTH_PORT = 1234
AUTH_FIRST_MESSAGE = "Введите ваше имя: "

sock = socket.socket()
sock.setblocking(True)


def connect_to_server():
    try:
        host = input("Введите адрес сервера: ")
        port = int(input("Введите порт: "))
        sock.connect((host, port))
    except Exception:
        sock.connect((DEFAULT_HOST, DEFAULT_PORT))

    while True:
        msg = input("Введите сообщение: ")
        if msg == "break":
            break
        sock.send(msg.encode())
        data = sock.recv(1024)
        sock.settimeout(None)
        print(data.decode())
    sock.close()


def connect_to_auth():
    try:
        sock.connect((AUTH_HOST, AUTH_PORT))
    except Exception:
        print("Ошибка подключения к серверу аутентификации")
    message = sock.recv(1024).decode()
    print(message)
    if message == AUTH_FIRST_MESSAGE:
        name = input()
        sock.send(name.encode())
    message = sock.recv(1024).decode()
    print(message)
    sock.close()


if __name__ == "__main__":
    # connect_to_server()
    connect_to_auth()