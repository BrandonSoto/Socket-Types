#!/usr/bin/env python

import socket
import time

server_name = 'localhost'
server_port = 4242

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(0, 25):
    message = 'message ' + str(i)
    client_socket.sendto(message, (server_name, server_port))
    receved_message, server_address = client_socket.recvfrom(2048)
    print 'Received: ', receved_message
    time.sleep(.5)

print 'Closed', client_socket.getsockname()
client_socket.close()


