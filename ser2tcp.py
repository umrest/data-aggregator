import serial
import socket
import time

class Ser2TCP():
    def __init__(self):
        self.ser = serial.Serial("COM12", 115200)
        self.serial_connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_connected = False
        self.socket_reconnect()

        # send identification byte
        data = bytearray(128)
        data[0] = 250
        data[1] = 3
        self.socket.send(data)

    def socket_reconnect(self):
        while not self.socket_connected: 
            print("Socket reconnect...")
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(.1)
                self.socket.connect(("127.0.0.1", 8091))
                self.socket_connected = True
            except:
                self.socket_connected = False
                time.sleep(1)
    
    def serial_reconnect(self):
        print("Serial reconnect...")
        self.serial_connected = True

    def run(self):
        while True:
            if not self.socket_connected:
                self.socket_reconnect()
            if not self.serial_connected:
                self.serial_reconnect()
            # Send serial data
            if self.ser.in_waiting > 0:
                try:
                    self.socket.send(self.ser.read(self.ser.in_waiting))
                    self.socket_connected = True
                except:
                    self.socket_connected = False
            try:
                data = self.socket.recv(128)
                self.socket_connected = True
                try:
                    self.ser.write(data)
                    self.ser.flush()
                    self.serial_connected = True
                except:
                    self.serial_connected = False
            except socket.timeout:
                pass
            except:
                self.socket_connected = False

s = Ser2TCP()
s.run()