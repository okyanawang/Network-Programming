import socket
import os

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 65432        # The port used by the server
CLIENT_DIR = os.path.dirname(os.path.realpath(__file__))

def receive_file(sock, filename):
    with open(os.path.join(CLIENT_DIR, 'files', filename), 'wb') as f:
        h = str(sock.recv(1024), 'utf-8')
        h2 = sock.recv(1024)
        print(h)
        all_data = b''
        while True:
            data = sock.recv(1024)
            # print(data)
            if data == b'':
                break
            if data.startswith(b'File not found'):
                print('File not found:', filename)
                break
            all_data += data
        # print(all_data)
        if filename not in os.listdir(CLIENT_DIR):
            print(f'Saving {filename} to {CLIENT_DIR}')
        f.write(all_data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        cmd = input('Enter a command: ').strip()
        s.sendall(cmd.encode())
        if cmd.startswith('download '):
            filename = cmd.split()[1]
            receive_file(s, filename)
            break
        else:
            response = s.recv(1024).decode().strip()
            print(response)
