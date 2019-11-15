#!/usr/bin/env python

# This script opens CONNECTIONS simultaneous connections to a remote socket,
# and sends a fixed string before closing the connection. The process is then
# repeated indefinitely

# Intended to unit test the tcp_server.py script

import asyncore
import socket
import time

from DataAggregator.ConnectionDefinitions.data import JoystickData

class Client(asyncore.dispatcher):
    host = "localhost"
    port = 5000
    mesg = b"Hello World\n"

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.reconnect()
        
    def reconnect(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, self.port))

    def handle_connect(self):
        print("Connect")

    def handle_close(self):
        self.close()

    def handle_read(self):
        self.recv(128)
        print("recieved")

    def writable(self):
        return True

    def handle_write(self):
        self.send(JoystickData().__bytes__())


def run():
    client = Client()

    asyncore.loop()

run()