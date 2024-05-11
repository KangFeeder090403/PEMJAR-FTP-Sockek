# PEMJAR-FTP-Socket
Nama : Alvito Uday Alfariz

NIM  : 1203220143



# **Deksripsi**
Program ini merupakan sebuah sistem File Transfer Protokol (FTP) sederharna yang dibuat menggunakan bahasa Python dengan protokol soket TCP/IP. Main program ini terdiri dari dua bagian code yaitu `client-side` dan juga` server-side`, yang dimana client-side berfungsi untuk mengirimkan perintah ke server dan menampilkan respon dari server, server sendiri berfungsi untuk menerima perintah dari client, melakukan perintah command yang diminta dan mengirim balasan data kembali ke client.



# **code client-side**
```ruby
   import socket
import sys
import os
import struct
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 1456
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connme():
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connected to server!")
    except:
        print("Connection failed! Make sure the server is running and the port is correct")


def upld(file_name):
    try:
        s.send(b"upload")
    except:
        print("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        file_size = os.path.getsize(file_name)
        s.send(struct.pack("i", file_size))
        start_time = time.time()
        print("Sending file...")
        content = open(file_name, "rb")
        l = content.read(BUFFER_SIZE)
        while l:
            s.send(l)
            l = content.read(BUFFER_SIZE)
        content.close()
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("f", time.time() - start_time))
        print("File sent successfully")
        return
    except:
        print("Error sending file")
        return

def list_files():
    try:
        s.send(b"ls")
    except:
        print("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        number_of_files = struct.unpack("i", s.recv(4))[0]
        for i in range(int(number_of_files)):
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size).decode()
            file_size = struct.unpack("i", s.recv(4))[0]
            print("\t{} - {}b".format(file_name, file_size))
            s.send(b"1")
        total_directory_size = struct.unpack("i", s.recv(4))[0]
        print("Total directory size: {}b".format(total_directory_size))
    except:
        print("Couldn't retrieve listing")
        return
    try:
        s.send(b"1")
        return
    except:
        print("Couldn't get final server confirmation")
        return

def dwld(file_name):
    try:
        s.send(b"download")
    except:
        print("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            print("File does not exist. Make sure the name was entered correctly")
            return
    except:
        print("Error checking file")
    try:
        s.send(b"1")
        output_file = open(file_name, "wb")
        bytes_received = 0
        print("\nDownloading...")
        while bytes_received < file_size:
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_received += BUFFER_SIZE
        output_file.close()
        print("Successfully downloaded {}".format(file_name))
        s.send(b"1")
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print("Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size))
    except:
        print("Error downloading file")
        return
    return

def delf(file_name):
    try:
        s.send(b"rm")
        s.recv(BUFFER_SIZE)
    except:
        print("Couldn't connect to server. Make sure a connection has been established.")
        return
    try:
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
    except:
        print("Couldn't send file details")
        return
    try:
        file_exists = struct.unpack("i", s.recv(4))[0]
        if file_exists == -1:
            print("The file does not exist on server")
            return
    except:
        print("Couldn't determine file existence")
        return
    try:
        confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
        while confirm_delete != "Y" and confirm_delete != "N" and confirm_delete != "YES" and confirm_delete != "NO":
            print("Command not recognized, try again")
            confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
    except:
        print("Couldn't confirm deletion status")
        return
    try:
        if confirm_delete == "Y" or confirm_delete == "YES":
            s.send(b"Y")
            delete_status = struct.unpack("i", s.recv(4))[0]
            if delete_status == 1:
                print("File successfully deleted")
                return
            else:
                print("File failed to delete")
                return
        else:
            s.send(b"N")
            print("Delete abandoned by user!")
            return
    except:
        print("Couldn't delete file")
        return

def get_file_size(file_name):
    try:
        s.send(b"size")
    except:
        print("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            print("File does not exist. Make sure the name was entered correctly")
            return
    except:
        print("Error checking file")
    try:
        s.send(b"1")
        print("File size: {} MB".format(file_size / 1024 / 1024))
        return
    except:
        print("Couldn't get final server confirmation")
        return

def quit():
    s.send(b"byebye")
    s.recv(BUFFER_SIZE)
    s.close()
    print("Server connection ended")
    return

print("Welcome to program ( BASIC )\n")
print("Command :")
print("connme              : Connect to server ( run first to connect server)")
print("upload <file_path>  : Upload file")
print("ls                  : List files")
print("download <file_path>: Download file")
print("rm <file_path>      : Delete file")
print("size <file_path>    : Get file size")
print("byebye              : Disconnect from server\n")


while True:
    prompt = input("\nEnter a command: ")
    if prompt[:6].lower() == "connme":
        connme()
    elif prompt[:6].lower() == "upload":
        upld(prompt[7:])
    elif prompt.lower() == "ls":
        list_files()
    elif prompt[:8].lower() == "download":
        dwld(prompt[9:])
    elif prompt[:2].lower() == "rm":
        delf(prompt[3:])
    elif prompt[:4].lower() == "size":
        get_file_size(prompt[5:])
    elif prompt.lower() == "byebye":
        quit()
        break
    else:
        print("Command not recognized; please try again")
```

# **code server-side**
```ruby
import socket
import sys
import time
import os
import struct

print("\nMenunggu Koneksi dari Client\n")

TCP_IP = "127.0.0.1"
TCP_PORT = 1456
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print("\n Connection with address : {}".format(addr))

def upld():
    conn.send(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()

    original_file_name = file_name
    counter = 1
    while os.path.exists(file_name):
        file_name = f"{os.path.splitext(original_file_name)[0]}_{counter}{os.path.splitext(original_file_name)[1]}"
        counter += 1

    conn.send(b"1")
    file_size = struct.unpack("i", conn.recv(4))[0]
    start_time = time.time()
    print(f"Receiving file: {file_name}")
    content = open(file_name, "wb")
    l = conn.recv(BUFFER_SIZE)
    while l:
        content.write(l)
        l = conn.recv(BUFFER_SIZE)
    content.close()
    conn.send(struct.pack("f", time.time() - start_time))
    conn.send(struct.pack("i", file_size))
    print("File received successfully")
    return

def list_files():
    print("Listing files...")
    listing = os.listdir(os.getcwd())
    conn.send(struct.pack("i", len(listing)))
    total_directory_size = 0
    for i in listing:
        conn.send(struct.pack("i", sys.getsizeof(i)))
        conn.send(i.encode())
        conn.send(struct.pack("i", os.path.getsize(i)))
        total_directory_size += os.path.getsize(i)
        conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("i", total_directory_size))
    conn.recv(BUFFER_SIZE)
    print("Successfully sent file listing")
    return

def dwld():
    conn.send(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        print("File name not valid")
        conn.send(struct.pack("i", -1))
        return
    conn.recv(BUFFER_SIZE)
    start_time = time.time()
    print("Sending file...")
    content = open(file_name, "rb")
    l = content.read(BUFFER_SIZE)
    while l:
        conn.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()
    conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("f", time.time() - start_time))
    print("File sent successfully")
    return

def delf():
    conn.send(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", 1))
    else:
        conn.send(struct.pack("i", -1))
    confirm_delete = conn.recv(BUFFER_SIZE).decode()
    if confirm_delete == "Y":
        try:
            os.remove(file_name)
            conn.send(struct.pack("i", 1))
        except:
            print("Failed to delete {}".format(file_name))
            conn.send(struct.pack("i", -1))
    else:
        print("Delete abandoned by client!")
        return

def get_file_size():
    conn.send(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        conn.send(struct.pack("i", -1))
    return

def quit():
    conn.send(b"1")
    conn.close()
    s.close()
    os.execl(sys.executable, sys.executable, *sys.argv)

while True:
    print("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE).decode()
    print("\nReceived instruction: {}".format(data))
    if data == "upload":
        upld()
    elif data == "ls":
        list_files()
    elif data == "download":
        dwld()
    elif data == "rm":
        delf()
    elif data == "size":
        get_file_size()
    elif data == "byebye":
        quit()
    data = None
```

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
