#! /usr/bin/env python3

import socket
import ssl
from urllib import request

HOST = "www.google.com"
SIZE = 1000


print("========= standard HTTP ============\n")

response = request.urlopen("http://" + HOST).read(SIZE)
print(response)
print("[truncated...]\n\n")


print("========== HTTP using TCP directly =============\n")

socket80 = socket.create_connection((HOST, 80))
request_bytes = """\
GET / HTTP/1.1
Host: {}

""".format(HOST).encode()
socket80.send(request_bytes)
response = socket80.recv(SIZE)
print(response)
print("[truncated...]\n\n")


print("========= standard HTTPS ============\n")

response = request.urlopen("https://" + HOST).read(SIZE)
print(response)
print("[truncated...]\n\n")


print("========== HTTPS using TLS directly =============\n")

socket443 = socket.create_connection((HOST, 443))
tls_connection = ssl.create_default_context().wrap_socket(
    socket443,
    server_hostname=HOST)
tls_connection.send(request_bytes)
response = tls_connection.recv(SIZE)
print(response)
print("[truncated...]\n\n")


print('======= HTTPS using TLS via "memory BIO" ==========\n')

socket443 = socket.create_connection((HOST, 443))
incoming_bio = ssl.MemoryBIO()
outgoing_bio = ssl.MemoryBIO()
tls_context = ssl.create_default_context()
tls_object = tls_context.wrap_bio(
    incoming_bio,
    outgoing_bio,
    server_hostname=HOST)

print(f"------- start handshake ----------")
while True:
    try:
        tls_object.do_handshake()
        break
    except ssl.SSLWantReadError:
        outgoing_bytes = outgoing_bio.read()
        if outgoing_bytes:
            socket443.sendall(outgoing_bytes)
            # What the heck are these bytes?
            # See https://tls13.ulfheim.net/
            print("SOCKET SENT:")
            print(outgoing_bytes)
            print()
        incoming_bytes = socket443.recv(SIZE)
        incoming_bio.write(incoming_bytes)
        print("SOCKET RECEIVED:")
        print(incoming_bytes)
        print()

print(f"------- handshake complete ({tls_object.version()}) ----------")
tls_object.write(request_bytes)
print("SENDING REQUEST:")
print(request_bytes)
print()
outgoing_bytes = outgoing_bio.read()
socket443.sendall(outgoing_bytes)
print("SOCKET SENT:")
print(outgoing_bytes)
print()
while True:
    incoming_bytes = socket443.recv(SIZE)
    incoming_bio.write(incoming_bytes)
    print("SOCKET RECEIVED:")
    print(incoming_bytes)
    print()
    try:
        response = tls_object.read(SIZE)
        print("RECEIVED RESPONSE:")
        print(response)
        print("[truncated...]")
        break
    except ssl.SSLWantReadError:
        continue
