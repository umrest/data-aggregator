import struct

JOYSTICK = 1
VISION = 2


JOYSTICK_PACKET = struct.Struct("dddddd")
VISION_PACKET = struct.Struct("dddddd")

PACKET = struct.Struct("B")