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
