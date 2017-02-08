#!/usr/bin/env python

import socket
import thread

print 'Setting up server...'

server_port = 12000
server_name = 'localhost'

handshake_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
handshake_socket.bind((server_name, server_port))
handshake_socket.listen(50)

print 'Server address =', handshake_socket.getsockname() 

print 'Server is setup and ready...'

def process_client(client_socket, client_address):
    message = ''
    print '\033[32mEstablished connection with', client_address, '\033[0m' 

    try:
        # close connection after last message comes through
        count = 0;
        while count < 25:
            message = client_socket.recv(1024)
            print 'Received ', message, 'from', client_address
            count += 1
            client_socket.send('Acknowledged ' + message)
    except socket.error, (value, message):
        print '\033[31mSocket error: ', message, '\033[0m'

    client_socket.close()
    print '\033[31mClosed connection with', client_address, '\033[0m'

while True:
    client_socket, client_address = handshake_socket.accept()
    thread.start_new_thread(process_client, (client_socket, client_address))



