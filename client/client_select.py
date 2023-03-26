import socket
import os

# HOST = socket.gethostname()  # The server's hostname or IP address
HOST = '192.168.253.227'
PORT = 65432        # The port used by the server
CLIENT_DIR = os.path.dirname(os.path.realpath(__file__))  # The client's current working directory

def receive_file(sock, filename):
    with open(os.path.join(CLIENT_DIR, 'files', filename), 'wb') as f:
        # Receive the title of the file from the server
        h = str(sock.recv(1024), 'utf-8')
        print(h)
        
        # Receive the contents of the file from the server
        all_data = b''
        while True:
            data = sock.recv(1024)
            if data == b'':
                break
            if data.startswith(b'File not found'):
                print('File not found:', filename)
                break
            all_data += data
        
        # Write the contents of the file to the local filesystem
        if filename not in os.listdir(os.path.join(CLIENT_DIR, 'files')):
            print(f'Saving {filename} to {CLIENT_DIR}/files')
        f.write(all_data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        # Prompt the user for a command to send to the server
        cmd = input('Enter a command: ').strip()
        s.sendall(cmd.encode())
        
        if cmd.startswith('download '):
            # If the command is "download", receive the file from the server
            filename = cmd.split()[1]
            receive_file(s, filename)
            break
        else:
            # If the command is invalid, print the server's response
            response = s.recv(1024).decode().strip()
            print(response)
