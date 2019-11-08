import asyncore
import logging
import socket

from .hero_serial import HeroSerial

from .datahandler import DataHandler

class AggregatorServer(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """
    
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(address)
        self.address = self.socket.getsockname()
        self.listen(1)
        self.hero_serial = HeroSerial("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0")
        return

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        DataHandler(sock=client_info[0], serial=self.hero_serial)
        return
    
    def handle_close(self):
        self.close()


def run():
    AggregatorServer(("0.0.0.0", 8091))
    asyncore.loop()