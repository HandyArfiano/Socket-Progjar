# Pemrograman Jaringan (Socket)

Nama : Handy Arfiano Hastyawan  
NIM : 1203220109

## Tugas Socket Client-Server (Single-Thread)

1. Membuat sebuah program server yang dapat menerima koneksi dari klien menggunakan protokol TCP. Server ini akan menerima pesan dari klien dan mengirimkan pesan balasan berisi jumlah karakter pada pesan tersebut. Gunakan port 12345 untuk server. Membuat analisa dari hasil program tersebut.

#### Server

Code:

![Code_Server](https://github.com/HandyArfiano/Socket-Progjar/blob/main/Images/Server-Karakter.png?raw=true)

Output:

![Output_Server](https://github.com/HandyArfiano/Socket-Progjar/blob/main/Images/Output_Server.png?raw=true)

Analisa:

Pada program “Server_1.py” dibuat menggunakan Python dan menggunakan modul socket untuk berkomunikasi melalui jaringan.
Langkah-langkah:
-	Mengimpor modul socket. Memuat pustaka yang diperlukan untuk komunikasi jaringan.
-	Membuat object socket, socket.AF_INET menunjukkan penggunaan protokol internet (IPv4) untuk komunikasi. socket.SOCK_STREAM menunjukkan penggunaan koneksi TCP yang berorientasi aliran (stream-oriented) dan dapat diandalkan (reliable).
-	Menentukan alamat host dan port untuk server.
-	Mengikat object socket pada server ke alamat dan port yang sudah ditentukan.
-	Menunggu koneksi masuk dari client.
-	Menerima koneksi dari client.
-	Menerima data dari client, lalu menghitung jumlah karakternya. Hasil decode data dari client.
-	Mengirim respons ke client. Dikirim respon berupa hasil encode
-	Menutup koneksi socket client dan server.
Fungsi utama program ini adalah:
-	Menerima pesan dari klien.
-	Menghitung jumlah karakter pada pesan tersebut.
-	Mengirimkan pesan balasan berisi jumlah karakter pada pesan tersebut.
-	Program “menggunakan protokol TCP untuk komunikasi antara server dan client.
Alamat host 127.0.0.1 adalah alamat loopback, yang berarti server dan client berada pada komputer yang sama. Port 12345 adalah port yang digunakan oleh server untuk mendengarkan koneksi dari client.

2. Membuat sebuah program klien yang dapat terhubung ke server yang telah dibuat pada soal nomor 1. Klien ini akan mengirimkan pesan ke server berupa inputan dari pengguna dan menampilkan pesan balasan jumlah karakter yang diterima dari server.

### Client

Code:
![Code_Client](https://github.com/HandyArfiano/Socket-Progjar/blob/main/Images/Client-Karakter.png?raw=true)

Output:

![Output_Client](https://github.com/HandyArfiano/Socket-Progjar/blob/main/Images/Output_Client.png?raw=true)

Analisa:
Pada program “Client_1.py” dibuat menggunakan Python dan menggunakan modul socket untuk berkomunikasi melalui jaringan.
Langkah-langkah:
-	Mengimpor modul socket. Memuat pustaka yang diperlukan untuk komunikasi jaringan.
-	Membuat objek socket. socket.AF_INET menunjukkan penggunaan protokol internet (IPv4) untuk komunikasi. socket.SOCK_STREAM menunjukkan penggunaan koneksi TCP yang berorientasi aliran (stream-oriented) dan dapat diandalkan (reliable).
-	Menentukan alamat host dan port dengan menetapkan server tujuan dengan alamat IP "127.0.0.1" dan port "12345".
-	Menghubungkan ke server. Membuka koneksi ke server yang ditentukan.
-	Mengirim pesan dengan meminta pengguna untuk memasukkan pesan, kemudian mengonversinya menjadi format byte (encode) dan mengirimkannya ke server.
-	Menerima respons pesan balasan dari server yang berisi jumlah karakter pada pesan yang dikirimkan.
-	Menampilkan respons pesan balasan dari server kepada pengguna dari format byte (decode).
-	Menutup koneksi jaringan dengan server.

Program ini mendemonstrasikan komunikasi jaringan dasar antara client dan server menggunakan modul socket Python. Client mengirimkan pesan ke server dan menerima balasan berisi jumlah karakter pada pesan tersebut. Pada program tersebut mengirim pesan “Handy Arfiano Hastyawan” dan dihitung jumlah karakternya oleh server. Hasil dari server dikirim kembali ke client lalu di tampilkan “Jumlah karakter dalam kalimat tersebut ada: 23” (Penghitungan karakter termasuk ‘space’).
