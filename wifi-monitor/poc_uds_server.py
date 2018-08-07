
import socket
import sys
import os
import pickle
from scapy.all import *

server_address = './uds'

try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
            raise

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

print('Starting server at address:' + server_address)

sock.bind(server_address)

sock.listen(1)

while True:
    print('Waiting for connection')
    connection, client_address = sock.accept()
    try:
        print('connection from '+str(client_address))
        i=0 
        while True:
            data = connection.recv(4096)
            if data:
                #print('Received['+ str(i)+']' + str(data))
                p = pickle.loads(data)

                #print(p.addr1)
                print(str(dir(p)))
                #print(str(len(p.payload)))
                i+=1
            else:
                print('client sent no more data')
                break
        else:
            print('No more data from client' + client_address)
            break

    finally:
        connection.close()

