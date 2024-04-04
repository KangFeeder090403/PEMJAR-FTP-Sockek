# PEMJAR-FTP-Socket
Nama : Alvito Uday Alfariz

NIM  : 1203220143



# **Deksripsi**
Program ini merupakan sebuah sistem File Transfer Protokol (FTP) sederharna yang dibuat menggunakan bahasa Python dengan protokol soket TCP/IP. Main program ini terdiri dari dua bagian code yaitu `client-side` dan juga` server-side`, yang dimana client-side berfungsi untuk mengirimkan perintah ke server dan menampilkan respon dari server, server sendiri berfungsi untuk menerima perintah dari client, melakukan perintah command yang diminta dan mengirim balasan data kembali ke client.



# **code client-side**
    import socket
    
    def run_client(host='localhost', port=12345):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
    
    try:
        while True:
            command = input("Masukan Perintah Command: ")

            if command == 'byebye':
                client_socket.sendall(command.encode())
                break

            elif command.startswith('download'):
                _, filename, new_filename = command.split()
                client_socket.sendall(f'download {filename}'.encode())
                response = client_socket.recv(1024).decode()

                if response == 'OK':
                    with open(new_filename, 'wb') as f:
                        while True:
                            data = client_socket.recv(1024)
                            if b'ENDOFFILE' in data:
                                f.write(data.replace(b'ENDOFFILE', b''))
                                break
                            f.write(data)
                    print(f"File {filename} downloaded as {new_filename}.")
                else:
                    print(response)

            elif command.startswith('upload'):
                _, filename, new_filename = command.split()
                client_socket.sendall(f'upload {filename} {new_filename}'.encode())
                response = client_socket.recv(1024).decode()

                if response == 'OK':
                    with open(filename, 'rb') as f:
                        chunk = f.read(1024)
                        while chunk:
                            client_socket.sendall(chunk)
                            chunk = f.read(1024)
                    print(f"File {filename} uploaded as {new_filename}.")
                else:
                    print(response)

            else:
                client_socket.sendall(command.encode())
                response = client_socket.recv(1024).decode()
                print("Respon:", response)
    
    finally:
        client_socket.close()
        
    if __name__ == "__main__":
        run_client()


# **code server-side**
    import os
    import socket

    def file_size(filename):
    return os.path.getsize(filename) / (1024 * 1024)

    def run_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server running on {host}:{port}")
    
    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")

            try:
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    print(f"Received command: {data}")

                    command = data.split()[0]
                    response = ''

                    if command == 'ls':
                        files = os.listdir('.')
                        response = '\n'.join(files)
                    elif command == 'rm':
                        filename = data.split()[1]
                        try:
                            os.remove(filename)
                            response = f"File {filename} deleted."
                        except FileNotFoundError:
                            response = "File not found."
                    elif command.startswith('download'):
                        _, filename = data.split()
                        try:
                            if not os.path.isfile(filename):
                                conn.sendall(b'ERROR: File not found.')
                            else:
                                conn.sendall(b'OK')
                                with open(filename, 'rb') as f:
                                    chunk = f.read(1024)
                                    while chunk:
                                        conn.sendall(chunk)
                                        chunk = f.read(1024)
                                conn.sendall(b'ENDOFFILE')
                                print(f"File {filename} has been sent.")
                        except Exception as e:
                            response = f"ERROR: {str(e)}"
                            conn.sendall(response.encode())
                    elif command.startswith('upload'):
                        _, filename, new_filename = data.split()
                        response = 'OK'.encode()
                        conn.sendall(response)
                        with open(new_filename, 'wb') as f:
                            while True:
                                data = conn.recv(1024)
                                if not data:
                                    break
                                f.write(data)
                        print(f"File uploaded as {new_filename}.")
                    elif command == 'size':
                        filename = data.split()[1]
                        try:
                            response = f"Size of {filename}: {file_size(filename):.2f} MB"
                        except FileNotFoundError:
                            response = "File not found."
                    elif command == 'byebye':
                        conn.close()
                        print("Connection closed.")
                        break
                    elif command == 'connme':
                        response = "Connection established."
                    else:
                        response = "Invalid command."
                    
                    conn.sendall(response.encode())

            finally:
                conn.close()

    finally:
        server_socket.close()

    if __name__ == "__main__":
    run_server()
    

# **1. Server**
Server berjalan dengan host `(localhost)` dan port `(12345)` dan menerima koneksi dari client secara terus menerus. Setelah dijalankan server menunggu koneksi dari client dan dapat menerima perintah dari client dan melakukan aksi opererasi sesuai dengan permintaan.

Berikut command yang tersedia :

+ `ls`
+ `rm`
+ `download`
+ `upload`
+ `size`
+ `byebye`
+ `conme`

# **2. Client**
Setelah sukses terhubung dengan server melalui host dan port yang ditentukan, pengguna dapat melakukan aksi operasi dengan memasukan command yang tersedia, lalu command akan dikirmkan ke server. 

Berikut tata cara menggunakan command yang tersedia pada program ini :

+ `ls` : digunakan untuk melihat daftar pada direktori yang ditempati server saat ini. Contoh output dan penggunaannya :
```
Masukan Perintah Command: ls
Respon: Mobalytics.lnk    
program
tempCodeRunnerFile.py     
testingall.rar
testing0.txt
testing01.txt
testing02.txt
testing03.txt
testing05.txt
```

+ `rm` : digunakan untuk menghapus file dalam satu direktori yang ditempati oleh server dengan acuan nama file pada parameter pertama. Contoh penggunaan command ini adalah dengan cara menginputkan `rm {nama_file}`. Jika sudah benar maka output akan  keluar output seperti ini :
```
Masukan Perintah Command: rm testing0.txt
Respon: File testing0.txt deleted.
```

+ `download` : digunakan untuk mengunduh file dari server degan acuan nama file yang diberikan pada parameter, contoh penggunaan dengan cara inputkan` download {nama_file_asal} {nama_file_tujuan}`. `{nama_file_asal}` adalah nama file diserver yang ingin diunduh, dan `{nama_file_tujuan}` adalah nama file yang akan disimpan di client. Jika sudah benar maka outpun akan keluar seperti ini :
```
Masukan Perintah Command: download testing01.txt testing0.txt   
File testing01.txt downloaded as testing0.txt.
```
Maka file `testing0.txt.` tadi yang sudah dihapus menggunakan command rm akan kembali ke direktori karena client melakukan unduhan terhadap file `testing0.txt.` dengan command download.

+ `upload` : digunakan untuk mengunggah file ke server, dengan cara server akan menyimpan dan menerima file unggahan berdasarkan acuan nama file. Contoh penggunaan dengan cara inputkan `upload {nama_file_asal} {nama_file_tujuan}`. `{nama_file_asal}` adalah nama file di client yang ingin di unggah, dan `{nama_file_tujuan}` adalah nama file yang akan disimpan di server. Jika sudah benar maka outpun akan keluar seperti ini :
```
Masukan Perintah Command: upload testing01.txt testing06.txt 
File testing01.txt uploaded as testing06.txt.
```

+ `Size` : digunakan untuk mengukur ukuran file diserver dengan satuan MB, cukup ketikan `size {nama_file}` maka outputnya akan seperti ini :
```
Masukan Perintah Command: size testingall.rar
Respon: Size of testingall.rar: 0.01 MB
```

+ `byebye` : digunakan untuk memutuskan koneksi dengan server. Output :
```
Masukan Perintah Command: byebye
PS C:\Users\ASUS\Desktop\Pemjar\tugas>
```

+ `connme` : digunakan untuk menguji koneksi dengan server, namun biasanya tidak digunakan secara manual oleh client. Output :
```
Masukan Perintah Command: connme
Respon: Connection established.
```
