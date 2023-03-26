import socket
import ssl

host = 'www.its.ac.id'
host2 = 'classroom.its.ac.id'
port = 443

# Nomer 1-3
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket = ssl.wrap_socket(client_socket)
# server_address = (host, port)
# client_socket.connect(server_address)

# request_header = b'GET https://www.its.ac.id/ HTTP/1.0\r\nHost: www.its.ac.id\r\n\r\n'
# client_socket.send(request_header)

# Nomer 4-5
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = ssl.wrap_socket(client_socket)
server_address = (host2, port)
client_socket.connect(server_address)

request_header = b'GET https://classroom.its.ac.id/ HTTP/1.0\r\nHost: classroom.its.ac.id\r\n\r\n'
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')
    
# Mendapatkan status code dari response header
status = response.split('\r\n')[0].split(maxsplit=1)[1]
status_code = status.split(maxsplit=1)[0]

# Menampilkan status code
print("NOMER 1")
print('Status code  :', status_code)
if status_code == '200':
    print('Description  : OK\n')
else:
    print('Description  :\n', response.split('\r\n\r\n')[0].split('HTTP/1.1 ')[1])

# Mengambil versi Content-Encoding dari HTTP response header
content_encoding = ''
for line in response.split('\r\n'):
    if 'Content-Encoding' in line:
        content_encoding = line.split(': ')[1]
        break

# Menampilkan versi Content-Encoding dari HTTP response header
print("NOMER 2")
if content_encoding:
    print('Content-Encoding : \n', content_encoding)
else:
    print('Content-Encoding tidak ditemukan\n')

# Mengambil versi HTTP dari HTTP response header
http_version = response.split('\r\n')[0].split(maxsplit=2)[0]

# Menampilkan versi HTTP dari HTTP response header
print("NOMER 3")
print('HTTP Version : ', http_version, '\n')

# Mendapatkan charset dari Content-Type
charset = ''
for line in response.split('\r\n'):
    if 'Content-Type' in line:
        content_type = line.split(': ')[1]
        charset = content_type.split('charset=')[1]
        break

# Menampilkan charset dari Content-Type
print("NOMER 4")
if charset:
    print('Charset  :', charset, '\n')
else:
    print('Charset tidak ditemukan \n')


client_socket.close()
