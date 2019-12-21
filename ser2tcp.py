import serial
import socket
import time
    

class Ser2TCP():
    def __init__(self):
        self.ser = serial.Serial("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0", 115200)
        self.serial_connected = True
        self.socket_connected = False
        self.socket_reconnect()


    def socket_reconnect(self):
        while not self.socket_connected: 
            print("Socket reconnect...")
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(10)
                
                self.socket.connect(("127.0.0.1", 8091))
                self.socket_connected = True
                identifier = bytearray(128)
                identifier[0] = 250
                identifier[1] = 3
                print("init")
                self.send_tcp(identifier)
            except:
                self.socket_connected = False
                time.sleep(1)
    
    def serial_reconnect(self):
        print("Serial reconnect...")
        self.serial_connected = True

    def recv_tcp(self):
        "Receive some data from the telnet client"
        try:
            data = self.socket.recv(128, socket.MSG_DONTWAIT)
            return data
        except socket.timeout:
            return None
        except:
            socket_connected = False

    def send_tcp(self, data):
        "Send some data out to the telnet client"
        try:
            self.socket.send(data)
        except:
            socket_connected = False
        

    def recv_serial(self):
        "Recieve some data from the serial port"
        while self.ser.in_waiting >= 128 + 3:
            key1 = self.ser.read(1)[0]
            if(key1 != 44):
                continue
            key2 = self.ser.read(1)[0]
            if(key2 != 254):
                continue
            key3 = self.ser.read(1)[0]
            if(key3 != 153):
                continue
            data = self.ser.read(128)
            return data

        return None

    def send_serial(self,data):
        "Send some data out to the serial port"
        print("Send serial")
        print(len(data))
        header = bytearray(3)
        header[0] = 44
        header[1] = 254
        header[2] = 153
        self.ser.write(header + data)

    def run(self):
        while True:
            if not self.socket_connected:
                self.socket_reconnect()
            if not self.serial_connected:
                self.serial_reconnect()
            data = self.recv_tcp()
            if data != None:
                self.send_serial(data)
            data = self.recv_serial()
            if data != None:
                self.send_tcp(data)


s = Ser2TCP()
s.run()