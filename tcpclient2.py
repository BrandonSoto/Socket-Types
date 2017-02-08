#!/usr/bin/env python

from socket import *
import time

server_port = 12000
server_name = 'localhost'

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

print '\033[33mClient connected with', client_socket.getsockname(), '\033[0m'

for i in range(0, 26):
    sent_message = 'message ' + str(i)
    print 'pushing message: "', sent_message, '"'
    client_socket.send(sent_message)
    print 'message sent!'
    time.sleep(.5)

print '\033[31mClosing socket ', client_socket.getsockname(), '\033[0m'
client_socket.close()
print 'Client done!'

