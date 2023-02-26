import socket
import os

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 65432        # The port used by the server
# CLIENT_DIR = '/path/to/client/folder'  # Change this to the path of your client folder
CLIENT_DIR = os.path.dirname(os.path.realpath(__file__))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        command = input('Enter command: ')
        if not command:
            break
        s.sendall(command.encode())
        data = s.recv(1024)
        if data == b'File not found':
            print('File not found')
        else:
            filename, file_data = data.split(b'\n', 1)
            with open(os.path.join(CLIENT_DIR, 'files', filename.decode()), 'wb') as f:
                f.write(file_data)
            print('File saved as', filename.decode())
            break
s.close()
print('Connection closed')
