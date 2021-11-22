#! /usr/bin/env python3

HOST = "www.google.com"
SIZE = 500

print("========== TCP =============")
import socket
socket80 = socket.create_connection((HOST, 80))
request = """\
GET / HTTP/1.1
Host: {}

""".format(HOST).encode()
socket80.send(request)
response = socket80.recv(SIZE)
print(response)
print()

print("========== TLS =============")
import ssl
socket443 = socket.create_connection((HOST, 443))
tls_connection = ssl.create_default_context().wrap_socket(
    socket443,
    server_hostname=HOST)
tls_connection.send(request)
response = tls_connection.recv(SIZE)
print(response)
print()

print("========= HTTPS ============")
from urllib import request
response = request.urlopen("https://" + HOST).read(SIZE)
print(response)
