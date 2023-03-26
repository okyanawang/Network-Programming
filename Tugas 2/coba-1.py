# import socket

# HOST = 'its.ac.id'  # The remote host
# PORT = 80               # The same port as used by the server

# # create a socket object
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # connect the socket to the remote host
# client_socket.connect((HOST, PORT))

# # send some data to the remote host
# request = b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n"
# client_socket.sendall(request)

# # receive the response from the remote host
# response = b""
# while True:
#     data = client_socket.recv(1024)
#     if not data:
#         break
#     response += data

# # print the response from the remote host
# print(response.decode())

# # close the socket
# client_socket.close()

import socket
import ssl
from bs4 import BeautifulSoup as soup

class HTTPS:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT

        self.connect()
        self.SSL()
        self.request()
        self.receive()
        self.save_response()
        self.get_status()
        self.get_encoding()
        self.get_httpver()
        self.get_charset()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))

    def SSL(self):
        context = ssl.create_default_context()
        self.sock = context.wrap_socket(self.sock, server_hostname=self.HOST)

    def request(self):
        self.sock.send(f"GET / HTTP/1.1\r\nHost:{self.HOST}\r\n\r\n".encode())

    def receive(self):
        self.response = ''
        while True:
            data = self.sock.recv(4096)
            self.response += data.decode('utf-8')
            if not data:
                self.sock.close()
                break
        self.response_len = len(self.response)
        self.header = self.response.split('<!DOCTYPE html>', maxsplit=1)[0]
        self.content = self.response.split('<!DOCTYPE html>', maxsplit=1)[1]
    
    def save_response(self):
        f = open(f"{self.HOST}_response.txt", "w+")
        f.write(self.response)
        f.close()

    def get_status(self):
        self.status = self.header.split("\r\n", 1)[0].split(maxsplit=1)[1]
        self.status_code = self.status.split()[0]
        self.status_desc = self.status.split()[1]
        print("\n")
        print(self.status)
        print(f"Status code\t: {self.status_code}")
        print(f"Status deskripsi: {self.status_desc}")

    def get_encoding(self):
        partition_header = self.header.split("\r\n")
        # Transfer-Encoding
        if any("Transfer-Encoding" in word for word in partition_header):
            self.transfer = list(filter(lambda a: 'Transfer-Encoding' in a, partition_header))[0]
            self.transfer =self.transfer.split()[1]
            print("\n")
            print(f"Transfer encoding: {self.transfer}")
        else:
            print("\nTransfer Encoding tidak ditemukan!")

        # Accept-Encoding
        if any("Accept-Encoding" in word for word in partition_header):
            self.accept = list(filter(lambda a: 'Accept-Encoding' in a, partition_header))[0]
            self.accept = self.accept.split()[0][:-1]
            print("\n")
            print(f"Accept Encoding: {self.accept}")
        else:
            print("\nAccept-Encoding tidak ditemukan!")
    
    def get_httpver(self):
        self.httpver = self.header.split("\r\n", 1)[0].split(maxsplit=1)[0]
        print("\n")
        print(f"Version: {self.httpver}")

    def get_charset(self):
        partition_header = self.header.split("\r\n")
        if any("charset" in word for word in partition_header):
            self.charset = list(filter(lambda a: 'charset' in a, partition_header))[0].split()[2]
            self.charset =self.charset.split("=",1)[1]
            print("\n")
            print(f"charset: {self.charset}")
        else:
            print("\nCharset tidak ditemukan!")

def parsing(response):
    doc = soup(response, "html.parser")
    direktori = []
    masuk_ul = doc.find("ul", {"class": "navbar-nav h-100 wdm-custom-menus links"})
    try:
        list_li = masuk_ul.find_all('li')
        for menu in list_li:
            panduan = menu.find('a')
            if panduan:
                direktori.append(panduan.text.strip())
            masuk_div = menu.find('div')
            dropdown = masuk_div.find_all('a')
            for dropDown in dropdown:
                direktori.append('\t' + dropDown.text.strip())
    except AttributeError:
        pass

    print("\nDaftar Menu :")
    for list_direktori in direktori:
        print(list_direktori)

# NOMOR 1 - 3
print("\n\nDomain : its.ac.id")
https = HTTPS("www.its.ac.id", 443)

# NOMOR 4 - 5
print("\n\nnDomain : classroom.its.ac.id")
https_2 = HTTPS("classroom.its.ac.id", 443)
parsing(https_2.response)