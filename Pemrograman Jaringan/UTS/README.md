# UTS | Pemrograman Jaringan

Nama : Handy Arfiano Hastyawan | NIM : 1203220109

Soal:

Buatlah sebuah permainan yang menggunakan soket dan protokol UDP. Permainannya cukup sederhana, dengan 1 server dapat melayani banyak klien (one-to-many). Setiap 10 detik, server akan mengirimkan kata warna acak dalam bahasa Inggris kepada semua klien yang terhubung. Setiap klien harus menerima kata yang berbeda (unik). Selanjutnya, klien memiliki waktu 5 detik untuk merespons dengan kata warna dalam bahasa Indonesia. Setelah itu, server akan memberikan nilai feedback 0 jika jawabannya salah dan 100 jika benar.

### How Code Works

#### Server.py

```
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
```

#### Output:

![Screenshot 2024-04-27 082820](https://github.com/HandyArfiano/Socket-Progjar/assets/162109542/3bcb8b1e-f97f-4c4f-81ac-03fe48ea1356)

Code ini meng-import `socket` untuk menyediakan fungsi soket dan `random` untuk menyediakan fungsi random yang dimana digunakan untuk menghasilkan warna secara acak. Fungsi `generatorWarnaRandom()` digunakan untuk memberikan warna acak. `warnaTersedia` adalah daftar yang berisi sepuluh nama warna dalam bahasa Indonesia. `random.choice(warnaTersedia)` digunakan untuk memilih warna acak dari daftar dan mengembalikannya.

Pada program `Server.py`

- `server_ip` diatur ke `"127.0.0.109"`, yang merupakan alamat loopback (localhost) pada program server.
- `server_port` diatur ke `12345`. Ini adalah nomor port yang akan di dengarkan server untuk pesan masuk.
- `server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)` membuat soket UDP. `AF_INET` menentukan alamat IPv4, dan `SOCK_DGRAM` menunjukkan soket datagram dalam UDP.
- `server_socket.bind((server_ip, server_port))` mengikat soket ke alamat IP dan port yang ditentukan.

Setelah itu program akan menampilkan alamat IP dan nomor port server, dan pesan yang menunjukkan bahwa server menunggu pesan dari klien.

`connected_clients` merupakan set yang akan menyimpan alamat klien yang terhubung. Set ini bermanfaat untuk menyimpan dan memeriksa keanggotaan secara efisien.

#### Loop Utama Server

Loop akan terus berjalan ulang tanpa henti hingga pengguna menghentikan program secara manual.

Menunggu Pesan dari Klien

Di dalam loop, server menggunakan `server_socket.recvfrom(1024)` untuk menunggu pesan dari klien. Setelah menerima data, server perlu mengubahnya menjadi string yang dapat dibaca. Ini dilakukan dengan menggunakan `data.decode("utf-8")`. Server kemudian memeriksa apakah klien yang mengirim pesan sudah terhubung sebelumnya. Ini dilakukan dengan menggunakan `client_address` dan mengeceknya pada set `connected_clients`.

`connected_clients` merupakan set yang menyimpan alamat IP dan port dari semua klien yang terhubung ke server. Set ini berguna untuk melacak klien yang terhubung dan menghindari pengiriman pesan berulang kali ke klien yang sama. `if client_address not in connected_clients` akan memeriksa alamat klien ada dalam set `connected_clients` atau tidak. Jika tidak ada, berarti ini adalah klien baru yang terhubung. Lalu, `connected_clients.add(client_address)` akan menambahkan alamat klien ke set `connected_clients`, menandakan bahwa klien tersebut sekarang terhubung.

Server akan memeriksa isi pesan yang diterima dari klien menggunakan if data == "Permintaan warna server". `data` diperoleh setelah men-decodekan byte yang diterima dari klien. Program akan memeriksa apakah isi pesan tersebut sama dengan "Permintaan warna server" (tanpa tanda kutip). Jika ya, berarti klien meminta warna acak dari server.

- `warna = generatorWarnaRandom()` merupakan fungsi yang dipanggil untuk menghasilkan warna acak. Fungsi ini memilih warna secara acak dari daftar warna yang tersedia ("merah", "pink", "oranye", ... , "white").
- `server_socket.sendto(warna.encode("utf-8"), client_address` digunakan server untuk mengirimkan warna yang dihasilkan `warna` kembali ke klien yang meminta.
  `.encode("utf-8")` digunakan untuk mengubah string warna menjadi byte sebelum dikirim, karena `sendto` hanya dapat mengirim data dalam bentuk byte.
- `sendto(warna.encode("utf-8"), client_address)` digunakan untuk mengirim data kembali ke klien yang meminta, menggunakan alamat IP dan port yang tersimpan di `client_address`.

Untuk menghentikan looping harus dilakukan secara manual. Penghentian manual ini biasanya dilakukan dengan menekan kombinasi tombol `Ctrl+C` pada keyboard.

- `except KeyboardInterrupt` digunakan untuk menangani except menggunakan pada program proses `try`...`except`
- `break` digunakan untuk keluar dari loop utama, sehingga program berhenti berjalan.

#### Penutupan Soket

Server perlu menutup soket yang digunakan untuk komunikasi. Ini dilakukan dengan `server_socket.close()`. Memastikan sistem yang digunakan oleh soket ditutup dengan benar.

### Client.py

```
import socket
import time
import threading

def translate_warna(warna_english):
    semua_warna = {
        "red": "merah",
        "pink": "merah muda",
        "orange": "oranye",
        "yellow": "kuning",
        "green": "hijau",
        "blue": "biru",
        "purple": "ungu",
        "brown": "coklat",
        "black": "hitam",
        "white": "putih",
    }
    return semua_warna.get(warna_english.lower(), "tidak valid")

server_ip = "127.0.0.109"
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



while True:
    try:
        def input_timeout(prompt ,timeout):
            print(prompt, flush=True)
            response = [None]
            def input_thread():
                try:
                    response[0] = input()
                except:
                    pass

            thread = threading.Thread(target=input_thread)
            thread.start()
            thread.join(timeout)

            if thread.is_alive():
                print(f"\nAnda tidak menjawab selama {timeout} detik\n")
                print("Tekan Enter untuk melanjutkan")
                thread.join()

                return None
            else:
                return response[0]

        client_socket.sendto("Permintaan warna server".encode("utf-8"), (server_ip, server_port))
        warna, server_address = client_socket.recvfrom(1024)
        warna = warna.decode("utf-8")
        print(f"Menerima warna: {warna}")

        response = input_timeout("Apa warna dalam bahasa Indonesia? ", 5)

        warna_indonesia = translate_warna(warna)
        if response is None:
            print("Waktu habis\nNilai: 0")
        elif response.lower() == warna_indonesia:
            print("Jawaban benar\nNilai: 100")
        else:
            print("Jawaban salah\nNilai: 0")

        print("\nAkan menerima warna baru dalam waktu 10 detik\n")
        time.sleep(10)
    except KeyboardInterrupt:
        print("\nKlien berhenti.")
        break

client_socket.close()
```

#### Output:

![Screenshot 2024-04-27 083213](https://github.com/HandyArfiano/Socket-Progjar/assets/162109542/2a23476a-bd0a-4bed-bcce-b4411a652b41)

Code ini mengimport `socket` untuk menyediakan fungsi soket. `time` untuk menyediakan fungsi waktu dan membuat penundaan. `threading` untuk menyediakan fungsi membuat dan mengelola threads, memungkinkan eksekusi kode secara bersamaan.

Fungsi `translate_warna(warna_english)` digunakan untuk menerjemahkan warna bahasa Inggris ke bahasa Indonesia.

- `semua_warna` variabel yang berisi nama warna bahasa Inggris ke bahasa Indonesia.
- `warna_english.lower()` untuk mengubah nama warna bahasa Inggris menjadi huruf kecil.
- `.get(key, default)` untuk memeriksa apakah kunci (nama warna bahasa Inggris) ada. Jika ya, nilai yang sesuai (terjemahan bahasa Indonesia) dikembalikan. Jika tidak, nilai default ("tidak valid") dikembalikan.

#### Menghubunkan pada Server

- `server_ip`: Alamat IP server yang ingin dihubungi klien.
- `server_port`: Port server yang ingin dihubungi klien.
- `client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`: Untuk membuat soket UDP pada klien.

#### Looping Utama Client

- `print(prompt, flush=True)`: Menampilkan prompt ke pengguna.
- `response = [None]`: Menginisialisasi daftar kosong untuk menyimpan respons pengguna.
- `def input_thread()`: Mendefinisikan sebagai thread terpisah untuk menangani input pengguna.
  - `try`: Mencoba mendapatkan input pengguna.
  - `except`: Menangani pengecualian (misalnya, menekan Ctrl+C) dan tidak melakukan apa-apa.
- `thread = threading.Thread(target=input_thread)`: Membuat thread baru untuk menjalankan fungsi `input_thread`.
- `thread.start()`: Memulai thread yang baru dibuat.
- `thread.join(timeout)`: Menunggu thread selesai dalam waktu `timeout` detik.
  - `if thread.is_alive()`: Memeriksa apakah thread masih berjalan.
    - `thread.join()`: Menunggu thread selesai.
  - else: Menjalankan jika thread selesai sebelum `timeout`.
- `return response[0]`: Mengembalikan respons pengguna.

#### Mengirim Permintaan Warna

`client_socket.sendto("Permintaan warna server".encode("utf-8"), (server_ip, server_port))`: Baris kode ini mengirim pesan "Permintaan warna server" ke server, menggunakan alamat IP dan port yang ditentukan.

#### Menerima Warna dari Server

- `warna, server_address = client_socket.recvfrom(1024)`: Baris kode ini menerima data dari server, menyimpan warna yang diterima dalam variabel warna dan alamat server dalam `server_address`.
- `warna = warna.decode("utf-8")`: Mengubah byte yang diterima menjadi string yang dapat dibaca.
- `response = input_timeout("Apa warna dalam bahasa Indonesia? ", 5)`: Mengirim prompt ke pengguna untuk menanyakan terjemahan warna ke bahasa Indonesia, dalam waktu 5 detik.
- `warna_indonesia = translate_warna(warna)`: Memanggil fungsi `translate_warna` untuk menerjemahkan warna bahasa Inggris ke bahasa Indonesia.

#### Penilaian

Klien disuruh untuk menjawab warna dari bahasa Inggris ke bahasa Indonesia. Apabilai tidak menjawab/jawabannya salah akan mendapatkan nilai 0, sedangkan apabila jawabannya benar akan mendapatkan niali 100

### Untuk menjalankan kode

1. Masuk ke dalam direktori kode yang akan dijalankan terlebih dahulu
2. Untuk menjalankan kode bisa menggunakan 2 cara:

- Menjalankan script `Proses.py` pada terminal
- Menjalankan script manual satu per satu dari mulai server dan semua clientnya. (Untuk mengetesnya bisa menjalankan satu client terlebih dahulu)

```
> python (nama script).py
```

![Screenshot 2024-04-27 082641](https://github.com/HandyArfiano/Socket-Progjar/assets/162109542/7d1229e5-3afb-49a5-8b0f-84a31b6d8adf)

Hasil dari Code semua dijalankan:
Server.py:

Server terhubung ke klien:

![Screenshot 2024-04-27 082820](https://github.com/HandyArfiano/Socket-Progjar/assets/162109542/3bcb8b1e-f97f-4c4f-81ac-03fe48ea1356)

Server mengirimkan warna ke klien:

![Screenshot 2024-04-27 083558](https://github.com/HandyArfiano/Socket-Progjar/assets/162109542/e0132a8b-0f9a-46b9-a8e6-c72fd4ebd568)

Client.py:

![Screenshot 2024-04-27 083213](https://github.com/HandyArfiano/Socket-Progjar/assets/162109542/2a23476a-bd0a-4bed-bcce-b4411a652b41)
