#!/usr/bin/python           # This is server.py file                                                                                                                                                                           

import socket               # Import socket module
import threading
from ConnectionDefinitions.BitArray8 import BitArray8
import time
from ConnectionDefinitions import TYPES

class SimpleRouter():
    def __init__(self):

        self.dashboard_socket = None
        self.hero_socket = None
        self.vision_socket = None

        self.vision_dashboard_timeout = 0

        self.dashboard_socket_lock = threading.Lock()
        self.vision_socket_lock = threading.Lock()
        self.hero_socket_lock = threading.Lock()

        self.s = socket.socket()         # Create a socket object
        
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
        self.s.bind(("0.0.0.0", 8091))        # Bind to the port
        
        self.s.listen(5)                 # Now wait for client connection.

    def update_socket(self, i, socket):
        if i == 1:
            self.dashboard_socket = socket
        if i == 2:
            self.vision_socket = socket
        if i == 3:
            self.hero_socket = socket
    
    def send_to_hero(self, msg):
        #print("Recieved Data for Hero")
        if self.hero_socket != None:
            self.hero_socket_lock.acquire()
            self.hero_socket.send(msg)
            self.hero_socket_lock.release()
        else:
            #print("Hero is not connected")
            pass
    
    def send_to_dashboard(self, msg):
        #print("Recieved Data for Dashboard")
        if self.dashboard_socket != None:
            self.dashboard_socket_lock.acquire()
            self.dashboard_socket.send(msg)
            self.dashboard_socket_lock.release()
        else:
            #print("Dashboard is not connected")
            pass

    def on_new_client(self, clientsocket,addr):
        i = -1
        try:
            while True:
                #while(clientsocket.recv(1, socket.MSG_WAITALL) != 255):
                #    print("Header invalid...")
                msg = clientsocket.recv(128, socket.MSG_WAITALL)
                if not msg:
                    break
                t = msg[0]
                # socket identification packet
                if t == TYPES.IDENTIFICATION:
                    i = msg[1]
                    print("Recieved Indetification Packet: ", i)
                    self.update_socket(i, clientsocket)
                # Vision, Dashboard, or joystick data gets sent to hero
                elif t == TYPES.VISION or t == TYPES.DASHBOARD or t == TYPES.JOYSTICK:
                    #print("Recieved Type ", t)
                    self.send_to_hero(msg)
                    if t == TYPES.VISION:
                        self.vision_dashboard_timeout += 1
                        if self.vision_dashboard_timeout >= 10:
                            self.vision_dashboard_timeout = 0
                            self.send_to_dashboard(msg)
                if t == TYPES.DASHBOARD_OUT:
                    self.send_to_dashboard(msg)
                else:
                    print("Invalid type: ", t)
        finally:
            clientsocket.close()
            self.update_socket(i, None)
        
    def send_dataaggregator_state(self):
        while True:
            data = bytearray(128)
            status = BitArray8()
            status.SetBit(0, self.hero_socket != None)
            status.SetBit(1, self.vision_socket != None)
            data[0] = TYPES.DATAAGGREGATOR
            data[1] = status.aByte[0]
            self.send_to_dashboard(data)
            time.sleep(1)
    
    def run(self):
        send_dataaggregator_state_thread = threading.Thread(target=self.send_dataaggregator_state)
        send_dataaggregator_state_thread.start()
        while True:
            c, addr = self.s.accept()     # Establish connection with client.
            print("Got connection from ", addr)
            t = threading.Thread(target=self.on_new_client,args=(c,addr))
            t.start()
        self.s.close()


s = SimpleRouter()
s.run()
