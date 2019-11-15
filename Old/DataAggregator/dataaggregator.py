import asyncore
import threading
import socket

import time

from .hero_serial import HeroSerial

from .datahandler import DataHandler

from .ConnectionDefinitions.BitArray8 import BitArray8

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
        self.hero_serial = HeroSerial("COM12")#"/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0")

        self.dashboard = None
        self.vision = None

        return

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        handler = DataHandler(sock=client_info[0], serial=self.hero_serial)
        if client_info[1][0] == "127.0.0.1":
            self.dashboard = handler
        return
    
    def handle_close(self):
        self.close()


def run():
    server = AggregatorServer(("0.0.0.0", 8091))
    thread = threading.Thread(target = asyncore.loop)
    thread.start()

    data = bytearray(128)
    data[0] = 8
    connected_status = BitArray8()
    connected_status.SetBit(0, server.hero_serial.connected)
    print(connected_status.GetBit(0))

    data[1] = connected_status.aByte[0]

    while True:
        if(server.dashboard == None):
            print("Dashboard not connected")
            time.sleep(1)
            continue
        server.dashboard.send(data)
        time.sleep(1)