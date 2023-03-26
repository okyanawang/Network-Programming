# imports the necessary modules: socket, select, sys, and os for socket programming, input/output operations, and system-specific parameters.
import socket
import select
import sys
import os

# imports the necessary modules: socket, select, sys, and os for socket programming, input/output operations, and system-specific parameters.
with open('httpserver.conf', 'r') as f:
    PORT = int(f.readlines()[1])

f.close()

# sets the current working directory to the directory containing the script file.
dir = os.path.dirname(os.path.realpath(__file__))

# creates a socket object, sets the socket options, binds it to the server address (localhost:PORT), and listens for incoming connections (up to 5).
server_address = ('localhost', PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

# creates a list input_socket containing the server_socket object.
input_socket = [server_socket]

# initiates an infinite loop that selects and returns the sockets that are ready for reading (read_ready), writing (write_ready), or have raised an exception (exception) using select.select() function.
try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        # checks if the ready socket is the server_socket object. If it is, it accepts the incoming connection, appends the new client socket object to the input_socket list. If not, it receives the data from the client through the connected socket object sock.recv() function, and breaks the loop when null is received.
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)                       
            
            else:                
                # receive data from client, break when null received          
                data = sock.recv(4096).decode('utf-8')

                # extracts the request header, checks if it is an empty string (which means that the client has closed the connection), and continues to the next iteration of the loop if so. It also initializes variables for the response header and data.
                request_header = data.split('\r\n')
                if request_header[0] == '':
                    sock.close()
                    input_socket.remove(sock)
                    continue

                request_file = request_header[0].split()[1]
                response_header = b''
                response_data = b''

                # checks if the requested file is index.html or /, and sends the contents of the file to the client. If not, it checks if the requested file is a directory, and sends the contents of the directory to the client. If not, it checks if the requested file exists, and sends the contents of the file to the client. If not, it sends a 404 Not Found response to the client.
                if request_file == 'index.html' or request_file == '/' or request_file == '/index.html':
                    f = open('index.html', 'r')
                    response_data = f.read()
                    f.close()
                    
                    content_len = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_len) + '\r\n\r\n'

                    sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                else:
                    file_path = dir + request_file
                    if os.path.isdir(file_path):
                        contents = os.listdir(file_path)
                        response_data = '<html><body><ul>'

                        for item in contents:
                            response_data += f'<li><a href="{request_file}/{item}">{item}</a></li>'
                        response_data += '</ul></body></html>'

                        content_len = len(response_data)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_len) + '\r\n\r\n'
                        sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                    elif os.path.exists(file_path):
                        if file_path.endswith('.html'):
                            with open(file_path, 'r') as f:
                                response_data = f.read()
                            content_len = len(response_data)
                            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_len) + '\r\n\r\n'
                            sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
                        
                        else:
                            with open(file_path, 'rb') as f:
                                response_data = f.read()
                            content_len = len(response_data)
                            response_header = 'HTTP/1.1 200 OK\r\nContent-Dispotition: attachment; filename="' + \
                                    os.path.basename(file_path) + \
                                    '"\r\nContent-Type: application/octet-stream\r\nContent-Length:' \
                                      + str(content_len) + '\r\n\r\n'
                            sock.sendall(response_header.encode('utf-8') + response_data)

                    else:
                        f = open(os.path.join(dir, '404.html'), 'r')
                        response_data = f.read()
                        f.close()

                        content_len = len(response_data)
                        response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                    + str(content_len) + '\r\n\r\n'
                        sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))


except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)
