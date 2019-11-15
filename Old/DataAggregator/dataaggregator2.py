import asyncio
from .dataprotocol import DataProtocol
from .hero_serial import HeroSerial
from .connections import Connections
from .ConnectionDefinitions.BitArray8 import BitArray8

import threading
import time
import struct

connections = Connections()

async def main(host, port):
    #hero_serial = HeroSerial("COM12")#"/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0")

    loop = asyncio.get_running_loop()
    
    server = await loop.create_server(lambda: DataProtocol(connections), host, port)

    await server.serve_forever()

def run():
    thread = threading.Thread(target = asyncio.run, args=(main('0.0.0.0', 8091), ))
    thread.start()

    while True:
        status = BitArray8()
        status.SetBit(0, connections.hero != None)
        status.SetBit(1, connections.vision != None)
        data = bytearray(128)
        data[0] = 8
        data[1] = status.aByte[0]
        if (connections.dashboard != None):
            connections.dashboard.send(data)
        time.sleep(1)