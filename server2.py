import socket
import logging
import datetime
import random

DEFAULT_PORT = 9090
DEFAULT_HOST = "localhost"

logger = logging.getLogger(__name__)
logging.basicConfig(filename='SERVER.log', filemode='w', level=logging.INFO)


class Server:
    def __init__(self):
        logger.info("Started")
        self.sock = socket.socket()
        try:
            host = input("Введите адрес сервера: ")
            port = int(input("Введите порт: "))
        except ValueError:
            host = DEFAULT_HOST
            port = DEFAULT_PORT
        try:
            self.sock.bind((host, port))
        except OSError:
            port = random.randint(1024, 49151)
            print("Указанный порт занят. Выбран случайный порт")
            self.sock.bind((host, port))
        self.sock.listen(0)
        print("Connected: host: {0}, port: {1}".format(host, port))
        logger.info("Connected: host: {0}, port: {1}".format(host, port))

    def listen(self):
        conn, addr = self.sock.accept()
        while True:
            data = conn.recv(1024)
            msg = data.decode("UTF-8")
            logger.info("message \"{0}\" received from client {1} at {2}"
                        .format(msg, addr, datetime.datetime.now()))
            conn.send(data)
            if msg == "exit":
                logger.info("Connection was closed")
                break
        conn.close()


def main():
    server = Server()
    server.listen()


if __name__ == "__main__":
    main()
