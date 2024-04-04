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
