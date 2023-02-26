import socket
import os

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 65432        # The port used by the server
# CLIENT_DIR = '/path/to/client/folder'  # Change this to the path of your client folder
CLIENT_DIR = os.path.dirname(os.path.realpath(__file__))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    command = input('Enter command: ')        
    
    s.sendall(command.encode())
    
    # 'File name: ' + filename + '\nFile size: ' + str(filesize) + ',\n'
    title = s.recv(1024).split(b'\n')
    filename = title[0].decode().split(" ")[2]
    filesize = title[1].decode().split(" ")[2]
    print('File name:', filename)
    print('File size:', filesize)
    all_data = b''
    while True:
        data = s.recv(1024)
        if data == b'File not found':
            print('File not found')
            break
            
        elif data == b'':
            break
        else:
            all_data = all_data + data
    with open(os.path.join(CLIENT_DIR, 'files', filename), 'wb') as f:
        f.write(all_data)
    print('File saved as', filename)
s.close()
print('Connection closed')
