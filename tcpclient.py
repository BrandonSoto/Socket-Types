#!/usr/bin/env python

from socket import *
import time

server_port = 12000
server_name = 'localhost'

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

for i in range(0, 26):
    sent_message = 'message ' + str(i)
    print 'sending message: "', sent_message, '"'
    client_socket.send(sent_message)
    print 'message sent!'

    print 'receiving message...'
    received_message = client_socket.recv(1024)
    print 'received "', received_message, '"'
    print 'server socket = '
    time.sleep(.5)

client_socket.close()
print 'Client done!'

