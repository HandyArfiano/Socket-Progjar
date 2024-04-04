# Pemrograman Jaringan | FTP Socket Programming

### Nama : Handy Arfiano Hastyawan | NIM : 1203220109

Soal:  
Buat sebuah program file transfer protocol menggunakan socket programming dengan beberapa perintah dari client seperti berikut:

- ls: ketika client menginputkan command tersebut, maka server akan memberikan daftar file dan folder
- rm (nama file): ketika client menginputkan command tersebut, maka server akan menghapus file dengan acuan nama file yang diberikan pada parameter pertama
- download (nama file): ketika client menginputkan command tersebut, maka server akan memberikan file dengan acuan nama file yang diberikan pada parameter pertama.
- upload (nama file): ketika client menginputkan command tersebut, maka server akan menerima dan menyimpan file dengan acuan nama file yang diberikan pada parameter pertama.
- size (nama file): ketika client menginputkan command tersebut, maka server akan memberikan informasi file dalam satuan MB (Mega bytes) dengan acuan nama file yang diberikan pada parameter pertama
- byebye: ketika client menginputkan command tersebut, maka hubungan socket client akan diputus.
- connme: ketika client menginputkan command tersebut, maka hubungan socket client akan terhubung.

## Jawaban

#### Server.py

```py
import socket
import os

SERVER_ADDRESS = ("localhost", 8001)
BUFFER_SIZE = 4096

server_directory = 'server'
if not os.path.exists(server_directory):
    os.makedirs(server_directory)

def list_files():
    files = os.listdir(server_directory)
    return "\n".join(files)

def delete_file(filename):
    path = os.path.join(server_directory, filename)
    try:
        os.remove(path)
        return f"File {filename} berhasil dihapus."
    except FileNotFoundError:
        return "File tidak ditemukan."

def get_file_size(filename):
    try:
        path = os.path.join(server_directory, filename)
        filesize = os.path.getsize(path)
        return f"Size: {filesize / 1024:.2f} KB"
    except FileNotFoundError:
        return "File tidak ditemukan."

def handle_command(conn, command):
    response = None
    if command.lower().startswith("ls"):
        response = list_files()
    elif command.startswith("rm"):
        _, filename = command.split(maxsplit=1)
        response = delete_file(filename)
    elif command.startswith("size"):
        _, filename = command.split(maxsplit=1)
        response = get_file_size(filename)
    elif command.startswith("download"):
        _, filename = command.split(maxsplit=1)
        file_path = os.path.join(server_directory, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    file_length = len(file_data)
                    conn.sendall(file_length.to_bytes(4, byteorder='big'))
                    conn.sendall(file_data)
                    # conn.sendall(f.read())
            except Exception as e:
                print(f"Gagal menerima file: {str(e)}")
        else:
            print("File tidak ditemukan pada server.")
    elif command.startswith("upload"):
        _, filename = command.split(maxsplit=1)
        try:
            file_size = int.from_bytes(conn.recv(4), byteorder='big')
            file_data = conn.recv(file_size)
            file_path = os.path.join(server_directory, filename)

            if not os.path.exists(server_directory):
                os.makedirs(server_directory)

            with open(file_path, "wb") as f:
                f.write(file_data)
            print(f"File {filename} berhasil diterima dan disimpan.")
        except Exception as e:
            print(f"Gagal menerima file: {str(e)}")
    elif command == "connme":
        response = "Berhasil terkoneksi antara server dan client"
    else:
        response = "Perintah tidak valid."

    if response:
        conn.send(response.encode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(SERVER_ADDRESS)
    s.listen()
    print("Menunggu Koneksi")
    conn, addr = s.accept()
    print("Berhasil Terkoneksi.")
    with conn:
        while True:
            command = conn.recv(BUFFER_SIZE).decode()
            if not command:
                break
            print(f"Menerima perintah: {command}")
            if command.lower() == "byebye":
                conn.send("Koneksi terputus dengan server.".encode())
                break
            if handle_command(conn, command):
                break
    conn.close()
```

#### Penjelasan:

1. list_files():

Fungsi ini membaca isi direktori server dan mengembalikan daftar nama file dalam format teks, dipisahkan dengan karakter baris baru.

2. delete_file(filename):

Fungsi ini menghapus file tertentu yang namanya sesuai dengan parameter filename. Fungsi ini akan mengembalikan pesan sukses jika berhasil menghapus atau pesan gagal jika file tidak ditemukan.

3. get_file_size(filename):

Fungsi ini mengembalikan ukuran file tertentu yang namanya sesuai dengan parameter filename. Ukuran file dikembalikan dalam format Kilobyte (KB) dengan dua angka di belakang koma. Jika file tidak ditemukan, fungsi ini akan mengembalikan pesan gagal.

4. handle_command(conn, command):

Fungsi ini merupakan fungsi utama untuk menangani perintah yang diterima dari client. Fungsi ini akan mengecek perintah tersebut dan menjalankan fungsi yang sesuai. Perintah yang didukung:

- ls: Menampilkan daftar file di server.
- rm filename: Menghapus file bernama filename.
- size filename: Menampilkan ukuran file bernama filename.
- download filename: Mengirimkan file bernama filename ke client.
- upload filename: Menerima file yang dikirimkan oleh client dan menyimpannya dengan nama filename di server.
- connme: Mengembalikan pesan sukses koneksi.
  Perintah lain yang tidak dikenali akan direspon dengan pesan "Perintah tidak valid."

```
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s::
```

Blok kode ini digunakan untuk membuat socket TCP server dan melakukan binding ke alamat yang ditentukan.

```
s.listen():
```

Membuat server listen untuk koneksi dari client.

```
conn, addr = s.accept():
```

Menunggu koneksi dari client dan menerima koneksi tersebut.

```
with conn::
```

Blok kode ini digunakan untuk memastikan koneksi dengan client ditutup dengan benar.

```
while True::
```

Loop yang terus berjalan hingga koneksi ditutup.

```
command = conn.recv(BUFFER_SIZE).decode():
```

Menerima perintah dari client dengan ukuran maksimum BUFFER_SIZE dan mengubahnya menjadi string.

```
if not command::
```

Jika tidak ada perintah yang diterima, loop akan dihentikan.

```
if command.lower() == "byebye"::
```

Jika client mengirimkan perintah "byebye", server akan mengirimkan pesan perpisahan dan menutup koneksi.

```
if handle_command(conn, command)::
```

Jika fungsi handle_command mengembalikan nilai True, loop akan dihentikan.

```
conn.close():
```

Menutup koneksi dengan client.

> Membuat socket menggunakan socket.socket(), mengikatnya ke alamat dan port tertentu dengan bind(), dan kemudian mendengarkan koneksi masuk dengan listen(). Ketika koneksi diterima, server menerima objek socket dan alamat dari klien yang terhubung menggunakan accept().  
> ...

...

#### Client.py

```py
import socket
import os

SERVER_ADDRESS = ("localhost", 8001)
BUFFER_SIZE = 4096

client_directory = 'client'
if not os.path.exists(client_directory):
    os.makedirs(client_directory)

def receive_file(s, filename):
    try:
        file_size = int.from_bytes(s.recv(4), byteorder='big')
        file_data = s.recv(file_size)
        file_path = os.path.join(client_directory, filename)

        if not os.path.exists(client_directory):
            os.makedirs(client_directory)

        with open(file_path, "wb") as f:
            f.write(file_data)
        print(f"File {filename} berhasil diterima.")
    except FileNotFoundError:
        print("Direktori untuk penyimpanan file tidak ada.")
    except Exception as e:
        print(f"Gagal menerima file: {str(e)}")

def sent_file(conn, filename):
    file_path = os.path.join(client_directory, filename)
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
                file_length = len(file_data)
                conn.sendall(file_length.to_bytes(4, byteorder='big'))
                conn.sendall(file_data)
            print(f"File {filename} berhasil dikirim.")
        except Exception as e:
            print(f"Gagal mengirim file: {str(e)}")
    else:
        print("File tidak ditemukan pada client.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Client sedang berjalan.")
    connected = False
    while True:
        command = input("\nSelamat datang dalam program FTP\nINSTRUKSI :\nconnme              : Connect to server\nupload <file_path>  : Upload file\nls                  : List files\ndownload <file_path>: Download file\nrm <file_path>      : Delete file\nsize <file_path>    : Get file size\nbyebye              : Keluar program\nMasukkan perintah:").strip()
        if not command:
            continue

        if command.lower() == 'connme':
            s.connect(SERVER_ADDRESS)

            s.send(command.encode())
            response = s.recv(BUFFER_SIZE).decode()
            print(response)
            connected = True
        elif connected:
            if command.lower() == 'ls':
                s.send(command.encode())
                response = s.recv(BUFFER_SIZE).decode()
                print(response)
            elif command.lower().startswith("rm"):
                s.send(command.encode())
                response = s.recv(BUFFER_SIZE).decode()
                print(response)
            elif command.lower().startswith("size"):
                s.send(command.encode())
                response = s.recv(BUFFER_SIZE).decode()
                print(response)
            elif command.lower().startswith("download"):
                s.send(command.encode())
                _, filename = command.split(maxsplit=1)
                receive_file(s, filename)
            elif command.lower().startswith("upload"):
                s.send(command.encode())
                _, filename = command.split(maxsplit=1)
                sent_file(s, filename)
            elif command.lower() == 'byebye':
                s.send(command.encode())
                response = s.recv(BUFFER_SIZE).decode()
                print(response)
                s.close()
                break
            else:
                response = "Invalid command."
                print(response)

        else:
            print("Client belum terhubung ke server.")

```

#### Penjelasan:

1. Fungsi `receive_file(s, filename):` Fungsi ini menerima file dari server. Fungsi ini akan menunggu ukuran file terlebih dahulu, kemudian membaca data file tersebut dan menyimpannya di direktori client dengan nama filename.

2. Fungsi `sent_file(conn, filename):` Fungsi ini mengirim file ke server. Fungsi ini akan membaca isi file yang berada di direktori client dengan nama filename, kemudian mengirimkan ukuran file dan isi file tersebut ke server.

- Looping program: Program ini menggunakan loop while True untuk terus berjalan hingga user memutuskan keluar. Di dalam loop ini, program akan meminta user untuk memasukkan perintah dan kemudian memproses perintah tersebut.
- Perintah if dan elif: Program menggunakan pernyataan if dan elif untuk mengecek perintah yang dimasukkan user dan kemudian menjalankan fungsi yang sesuai.

Program client FTP sederhana yang digunakan untuk melakukan berbagai operasi transfer file dengan server FTP.

#### Jalannya program:

1. Program membuat socket TCP client.
2. Program menampilkan pesan "Client sedang berjalan." dan variable connected di set menjadi False (belum terhubung).
3. Program masuk ke dalam loop yang terus berjalan hingga user memutuskan keluar.
   Di dalam loop, program menampilkan menu berisi perintah-perintah yang tersedia:

- connme: Menyambungkan ke server.
- upload <file_path>: Mengirimkan file ke server.
- ls: Menampilkan daftar file di server.
- download <file_path>: Mengunduh file dari server.
- rm <file_path>: Menghapus file di server.
- size <file_path>: Mengetahui ukuran file di server.
- byebye: Keluar dari program dan memutuskan koneksi.

4. User kemudian memasukkan perintah yang diinginkan.
5. Perintah tersebut kemudian diperiksa menggunakan kondisi if dan elif.

- Jika `connme:` client akan mencoba terhubung ke server menggunakan alamat yang ditentukan di `SERVER_ADDRESS`. Jika berhasil terhubung, variable `connected` akan diubah menjadi `True`.
- Jika sudah terhubung (connected bernilai True) dan perintahnya sesuai:
- `ls`: client akan mengirimkan perintah `ls` ke server dan menampilkan respon berupa daftar file di server.
- `rm, size, download:` Perintah dan nama file akan dikirimkan ke server. Server kemudian akan memproses perintah tersebut dan mengirimkan respon ke client.
- `upload:` client akan mengirimkan perintah upload dan nama file ke server. Kemudian fungsi sent_file akan dipanggil untuk mengirim isi file ke server.
- `byebye:` client akan mengirimkan perintah byebye ke server, menampilkan respon server, dan menutup koneksi.
  Perintah lain yang tidak dikenali akan direspon dengan pesan "Invalid command."  
  Jika client belum terhubung (connected bernilai False), program akan menampilkan pesan "Client belum terhubung ke server."

#### Cara menjalankan program:

Cara menjalankan program FTP Socket Programming:

Jalankan `Server.py` dengan mengetikkan pada terminal:

```
> python Server.py
```

Kemudian jalankan juga `Client.py` dengan mengetikkan pada terminal:

```
> python Client.py
```

Maka akan pada server akan muncul tulisan `menunggu koneksi` pada server dan pada client akan muncul tulisan

```
SELAMAT DATANG PADA PROGRAM FTP
INSTRUKSI :
upload <file_path>  : Upload file
ls                  : List files
download <file_path>: Download file
rm <file_path>      : Delete file
size <file_path>    : Get file size
byebye              : Keluar program
Masukkan perintah:
```

#### Command

- Upload <file_path>  
  Digunakan untuk mengirimkan file ke server.

```
upload D:\Kuliah\Semester 4\Pemrograman Jaringan\server\file1.txt
```

Maka akan muncul `File D:\Kuliah\Semester 4\Pemrograman Jaringan\server\File2.txt berhasil dikirim.`

- ls  
  Digunakan untuk menampilkan daftar file di server. Makan akan muncul list yang ada dalam folder D:\Kuliah\Semester 4\Pemrograman Jaringan\server

- download
  Digunakan untuk mengunduh file dari server.

```
download D:\Kuliah\Semester 4\Pemrograman Jaringan\server\Profil.txt
```

Maka akan muncul `File D:\Kuliah\Semester 4\Pemrograman Jaringan\server\Profil.txt berhasil diterima.`

- rm
  Digunakan untuk menghapus file di server.

```
rm File 2
```

Maka akan muncul `File File2 berhasil dihapus.`

- Size
  Digunakan untuk mengetahui ukuran file di server.

```
size Profil.txt
```

Maka akan muncul `Size: 0.07 KB`

- byebye
  Digunakan untuk keluar dari program dan memutuskan koneksi. Setelah melakukan command tersebut maka client akan terputus dengan server `Koneksi terputus dengan server.`
