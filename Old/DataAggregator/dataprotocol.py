import asyncio
from .ConnectionDefinitions.TYPES import JOYSTICK, VISION, DASHBOARD, HERO

class DataProtocol(asyncio.Protocol):

    def __init__(self, connections):
        print("Connection Started")
        self.connections = connections

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        t = data[0]
        if (t == JOYSTICK):
            print("Recieved Joystick Data")
            if(self.connections.hero != None):
                self.connections.hero.send(data)

        elif (t == VISION):
            print("Recieved Vision Data")
            if(self.connections.hero != None):
                self.connections.hero.send(data)
        
        elif (t == DASHBOARD):
            print("Recieved Dashboard Data")
            if(self.connections.hero != None):
                self.connections.hero.send(data)

        elif (t == HERO):
            print("Recieved Hero Data")
            if(self.connections.dashboard != None):
                self.connections.dashboard.send(data)
        
        elif (t == 250):
            print("Recieved Connected Identifier")
            if(data[1] == 1):
                self.connections.dashboard = self
            if(data[1] == 2):
                self.connections.vision = self
            if(data[1] == 3):
                self.connections.hero = self
        
        else:
            print ("Recieved Invalid data type: ", t)
        
    def send(self, data):
        self.transport.write(data)
