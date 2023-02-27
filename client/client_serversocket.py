import socket
import os

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 65432        # The port used by the server
# CLIENT_DIR = '/path/to/client/folder'  # Change this to the path of your client folder
CLIENT_DIR = os.path.dirname(os.path.realpath(__file__))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    command = input('Enter command: ')        
    
    # Send the command entered by the user to the server
    s.sendall(command.encode())
    
    # Receive the file information from the server
    title = s.recv(1024).split(b'\n')
    filename = title[0].decode().split(" ")[2]
    filesize = title[1].decode().split(" ")[2]
    print('File name:', filename)
    print('File size:', filesize)
    
    all_data = b''
    while True:
        # Receive the file data from the server
        data = s.recv(1024)
        if data == b'File not found':
            # If the file is not found on the server, print a message and break the loop
            print('File not found')
            break
        elif data == b'':
            # If there is no more data to receive, break the loop
            break
        else:
            # Append the received data to the file data
            all_data = all_data + data
    
    # Write the file data to a file in the client directory
    with open(os.path.join(CLIENT_DIR, 'files', filename), 'wb') as f:
        f.write(all_data)
    print('File saved as', filename)

# Close the socket connection
s.close()

print('Connection closed')
