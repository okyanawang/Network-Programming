import socket
import os
import select

HOST = socket.gethostname()
# HOST = '192.168.1.2'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
SERVER_DIR = os.path.dirname(os.path.realpath(__file__))

def send_file(conn, filename, filesize):
    try:
        with open(os.path.join(SERVER_DIR, 'files', filename), 'rb') as f:
            file_data = f.read()
        # print('Sending', filename)
        title = 'File name: ' + filename + '\nFile size: ' + str(filesize) + ',\n'
        conn.send(title.encode())
        conn.sendall(file_data)
        print('Sent', filename)
    except FileNotFoundError:
        conn.sendall(b'File not found')
        print('File not found:', filename)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print('Server listening on', HOST, PORT)

    # Create a list of active sockets that includes the server socket
    sockets = [s]

    try:
        while sockets:
            # Use select to wait for any of the sockets in the list to become readable
            readable, _, _ = select.select(sockets, [], [])

            for sock in readable:
                if sock is s:
                    # If the server socket is readable, accept the connection and add the new socket to the list
                    conn, addr = s.accept()
                    print('Connected by', addr)
                    sockets.append(conn)
                else:
                    # If a client socket is readable, receive the data and handle the command
                    data = sock.recv(1024).decode().strip()
                    if not data:
                        # If the socket is closed, remove it from the list
                        print('Disconnected from', sock.getpeername())
                        sockets.remove(sock)
                    elif data.startswith('download '):
                        # If the command is "download", send the requested file and remove the socket from the list
                        filesize = os.path.getsize(os.path.join(SERVER_DIR, 'files', data.split()[1]))
                        print('File size:', filesize)
                        filename = data.split()[1]
                        send_file(sock, filename, filesize)
                        sock.close()
                        sockets.remove(sock)
                    else:
                        # If the command is invalid, send an error message and remove the socket from the list
                        sock.sendall(b'Invalid command')
                        print('Invalid command:', data)
                        sock.close()
                        sockets.remove(sock)
    except KeyboardInterrupt:
        print('Server shutting down')
        s.close()
        print('Server closed')
