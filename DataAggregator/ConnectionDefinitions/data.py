import struct

from .TYPES import *

class JoystickData():
    def __init__(self, b=None):
        if b != None:
            joystick_data = b[:50]
            self.buttons_1, self.buttons_2, self.lj_x, self.lj_y, self.rj_x, self.rj_y, self.lt, self.rt = JOYSTICK_PACKET.unpack(joystick_data)
        else:
            self.lj_x, self.lj_y, self.rj_x, self.rj_y, self.lt, self.rt = (0,0,0,0,0,0)

    def __bytes__(self):
        joystick_data = JOYSTICK_PACKET.pack(self.lj_x, self.lj_y, self.rj_x, self.rj_y, self.lt, self.rt)
        ret = PACKET.pack(JOYSTICK) + joystick_data + bytearray(128 - 1 - len(joystick_data))
        return ret
    
    def __str__(self):
        return """
        Left Joystick:
            X: {0:.2f} Y: {1:.2f}
        Right Joystick:
            X: {2:.2f} Y: {3:.2f}
        Left Trigger:
            {4:.2f}
        Right Trigger:
            {5:.2f}
        Buttons:
            {6} {7}
        """.format(self.lj_x, self.lj_y, self.rj_x, self.rj_y, self.lt, self.rt, self.buttons_1, self.buttons_2)

class VisionData():
    def __init__(self, b=None):
        if b != None:
            vision_data = b[:48]
            self.yaw, self.pitch, self.roll, self.x, self.y, self.z = VISION_PACKET.unpack(vision_data)
        else:
            self.yaw, self.pitch, self.roll, self.x, self.y, self.z = (0,0,0,0,0,0)
            
    def __bytes__(self):
        joystick_data = VISION_PACKET.pack(self.yaw, self.pitch, self.roll, self.x, self.y, self.z)
        ret = PACKET.pack(VISION) + joystick_data + bytearray(128 - 1 - len(joystick_data))
        return ret
    
    def __str__(self):
        return """
        Angle:
            Y: {0:.2f} P: {0:.2f} R: {0:.2f}
        Position:
            X: {0:.2f} Y: {0:.2f} Z: {0:.2f}
        """.format(self.yaw, self.pitch, self.roll, self.x, self.y, self.z)