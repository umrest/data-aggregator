import asyncio
from .ConnectionDefinitions.TYPES import JOYSTICK, VISION, DASHBOARD

class DataProtocol(asyncio.Protocol):

    def __init__(self, serial):
        print("Connection Started")
        self.serial = serial

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        t = data[0]
        if (t == JOYSTICK):
            print("Recieved Joystick Data")
            self.serial.send(data)

        if (t == VISION):
            print("Recieved Vision Data")
            self.serial.send(data)
        
        if (t == DASHBOARD):
            print("Recieved Dashboard Data")
            self.serial.send(data)