import asyncore
import logging
import socket

from .datahandler import DataHandler

class AggregatorServer(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """
    
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()
        self.listen(1)
        return

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        DataHandler(sock=client_info[0])
        return
    
    def handle_close(self):
        self.close()


def run():
    AggregatorServer(("0.0.0.0", 5000))
    asyncore.loop()