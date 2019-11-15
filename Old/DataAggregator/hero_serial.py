import serial
import threading

class HeroSerial():
    def __init__(self, port):
        self.port = port
        self.baud = "115200"
        self.timeout = 1

        self.try_connect()

        self.lock = threading.Lock()
    
    def try_connect(self):
        try:
            self.ser=serial.Serial(self.port,self.baud,timeout=self.timeout)
            self.connected = True
        except:
            self.connected = False
        
    def send(self, b):
        if not self.connected:
            self.try_connect()
        # failed to connect again...
        if not self.connected:
            print("Serial not connected")
            return False
        
        self.lock.acquire()
        self.ser.write(b)
        self.ser.flush()
        self.lock.release()
        return True
    
    def recieve(self, b):
        if not self.connected:
            print("Serial not connected")
            return False

        if(self.ser.in_waiting >= 128):
            print("Serial data recieved, sending")
            self.lock.acquire()
            b = self.ser.read(128)
            self.lock.release()
            return True
        
        return False

