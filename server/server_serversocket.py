# import socket
# import os

# HOST = socket.gethostname()  # Standard loopback interface address (localhost)
# PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
# # SERVER_DIR = '/path/to/server/folder'  # Change this to the path of your server folder
# SERVER_DIR = os.path.dirname(os.path.realpath(__file__))

# def send_file(conn, filename):
#     try:
#         with open(os.path.join(SERVER_DIR, 'files', filename), 'rb') as f:
#             file_data = f.read()
#         conn.sendall(filename.encode() + b'\n' + file_data)
#         print('Sent', filename)
#     except FileNotFoundError:
#         conn.sendall(b'File not found')
#         print('File not found:', filename)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     print('Server listening on', HOST, PORT)
#     conn, addr = s.accept()
#     print('Connected by', addr)
#     while True:
#         data = conn.recv(1024).decode().strip()
#         if not data:
#             break
#         if data.startswith('download '):
#             filename = data.split()[1]
#             send_file(conn, filename)
#             break
#         else:
#             conn.sendall(b'Invalid command')
#             print('Invalid command:', data)
#     conn.close()


# Punyaku yang ini
import socket
import os

HOST = socket.gethostname()  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
# SERVER_DIR = '/path/to/server/folder'  # Change this to the path of your server folder
SERVER_DIR = os.path.dirname(os.path.realpath(__file__))

def send_file(conn, filename, filesize):
    try:
        with open(os.path.join(SERVER_DIR, 'files', filename), 'rb') as f:
            file_data = f.read()
        title = 'File name: ' + filename + '\nFile size: ' + str(filesize) + ',\n'
        conn.send(title.encode())
        conn.sendall(file_data)
        print('Sent', filename)
    except FileNotFoundError:
        conn.sendall(b'File not found')
        print('File not found:', filename)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server listening on', HOST, PORT)
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        if data.startswith('download '):
            filename = data.split()[1]
            filesize = os.path.getsize(os.path.join(SERVER_DIR, 'files', data.split()[1]))
            print('File name:', filename)
            print('File size:', filesize)
            send_file(conn, filename, filesize)
            break
        else:
            conn.sendall(b'Invalid command')
            print('Invalid command:', data)
    conn.close()
