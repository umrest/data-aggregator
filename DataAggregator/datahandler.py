import asyncore
import logging

from .ConnectionDefinitions.data import JoystickData, VisionData
from .ConnectionDefinitions.TYPES import JOYSTICK, VISION

class DataHandler(asyncore.dispatcher_with_send):
    """
        Recieves all data from all clients, and figures out what to do with them all
    """

    def handle_read(self):
        data = self.recv(128)
        if(data):
            t = data[0]
            if (t == JOYSTICK):
                joy = JoystickData(data[1:])
                print("Recieved Joystick Data: \n", joy)

                # TODO send to HERO


            if (t == VISION):
                vision = VisionData(data[1:])
                print("Recieved Vision Data: \n", vision)
            
                # TODO send to HERO
            
            

