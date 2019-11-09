class BitArray8:
    def __init__(self):
        self.aByte = bytearray(1)

    def SetBit(self, pos: int, value: bool):
        if value:
            self.aByte[0] = (self.aByte[0] | (1 << pos))
            
        else:
            self.aByte[0] = (self.aByte[0] & ~(1 << pos))

    def GetBit(self, pos: int):
        return (self.aByte[0] & (1 << pos)) != 0