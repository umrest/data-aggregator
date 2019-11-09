import asyncio
from .dataprotocol import DataProtocol
from .hero_serial import HeroSerial


async def main(host, port):
    hero_serial = HeroSerial("COM5")#"/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0")

    loop = asyncio.get_running_loop()
    
    server = await loop.create_server(lambda: DataProtocol(hero_serial), host, port)

    await server.serve_forever()

def run():
    asyncio.run(main('0.0.0.0', 8091))