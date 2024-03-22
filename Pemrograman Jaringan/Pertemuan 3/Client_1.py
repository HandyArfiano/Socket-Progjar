import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = 'localhost'
PORT = 12345

client_socket.connect((HOST, PORT))
pesanKata = input("Masukkan karakter : ")

client_socket.sendall(pesanKata.encode())
data = client_socket.recv(1024)

print(data.decode())
client_socket.close()