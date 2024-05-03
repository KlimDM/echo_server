import socket

sock = socket.socket()
try:
	host = input("Введите адрес сервера: ")
	port = int(input("Введите порт: "))
except ValueError:
	host = 'localhost'
	port = 9090
sock.bind((host, port))
print("Connected: host: {0}, port: {1}".format(host, port))
sock.listen(0)

conn, addr = sock.accept()
print("Client {0} connected".format(addr))

msg = ""


while True:
	data = conn.recv(1024)
	data.decode()
	conn.send(data)
	print("message \"{0}\" received from client {1}".format(data.decode(), addr))

print(msg)

conn.close()
