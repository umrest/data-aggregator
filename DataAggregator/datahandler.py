import asyncore
import logging

from .ConnectionDefinitions.data import JoystickData, VisionData
from .ConnectionDefinitions.TYPES import JOYSTICK, VISION, DASHBOARD

class DataHandler(asyncore.dispatcher_with_send):
    """
        Recieves all data from all clients, and figures out what to do with them all
    """

    def __init__(self, sock, serial):
        super().__init__(sock=sock)
        self.serial = serial


    def handle_read(self):
        data = self.recv(128)
        if(data):
            t = data[0]
            if (t == JOYSTICK):
                print("Recieved Joystick Data")

                # TODO send to HERO

                self.serial.send(data)


            if (t == VISION):
                print("Recieved Vision Data")
            
                # TODO send to HERO

                self.serial.send(data)
            
            if (t == DASHBOARD):
                print("Recieved Dashboard Data")

                
                # send to hero
                self.serial.send(data)
            

