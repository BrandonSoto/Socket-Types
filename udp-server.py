#!/usr/bin/env python

import socket

server_name = 'localhost'
server_port = 4242

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_name, server_port))

print 'Server is ready...'

while True:
    try:
        message, client_address = server_socket.recvfrom(2048)

        print 'Received -', message

        server_socket.sendto(message.upper(), client_address)
    except socket.error, (message, value):
        print 'socket error:', message
