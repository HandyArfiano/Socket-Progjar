import socket
import random

def generatorWarnaRandom():
    warnaTersedia = ["red", "pink", "orange", "yellow", "green", "blue", "purple", "brown", "black", "white"]
    return random.choice(warnaTersedia)

server_ip = "127.0.0.109"
server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"Server IP: {server_ip}\nServer port:{server_port}")
print("Menunggu pesan dari client...")

connected_clients = set()

while True:
    try:
        data, client_address = server_socket.recvfrom(1024)
        data = data.decode("utf-8")

        if client_address not in connected_clients:
            connected_clients.add(client_address)
            print(f"Klien terhubung dari {client_address}")

        if data == "Permintaan warna server":
            warna = generatorWarnaRandom()
            server_socket.sendto(warna.encode("utf-8"), client_address)
            print(f"Kirim warna {warna} ke {client_address}")

    except KeyboardInterrupt:
        print("\nServer berhenti.")
        break

server_socket.close()