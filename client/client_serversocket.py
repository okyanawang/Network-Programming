import socket
import os

HOST = '192.168.43.227'
# HOST = socket.gethostname()  # The server's hostname or IP address
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
    
    all_data = b'' # Inisialisasi variabel all_data sebagai sebuah string kosong

    while True: # Mulai loop
        # Menerima data dari server menggunakan s.recv() dengan ukuran maksimum 1024 bytes
        data = s.recv(1024) 
        
        if data == b'File not found': # Jika pesan "File not found" diterima dari server,
            print('File not found')  # cetak pesan "File not found"
            break                    # hentikan loop
            
        elif data == b'': # Jika tidak ada data lagi yang diterima dari server,
            break         # hentikan loop
            
        else: # Jika ada data yang diterima dari server,
            all_data = all_data + data # tambahkan data tersebut ke variabel all_data
            
    # Setelah loop selesai, variabel all_data akan berisi seluruh data file yang diterima dari server.

    
    # Write the file data to a file in the client directory
    with open(os.path.join(CLIENT_DIR, 'files', filename), 'wb') as f:
        f.write(all_data)
    print('File saved as', filename)

# Close the socket connection
s.close()

print('Connection closed')
