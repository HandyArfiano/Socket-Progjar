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
