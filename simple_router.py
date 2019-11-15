#!/usr/bin/python           # This is server.py file                                                                                                                                                                           

import socket               # Import socket module
import threading

class SimpleRouter():
    def __init__(self):

        self.dashboard_socket = None
        self.hero_socket = None
        self.vision_socket = None

        self.s = socket.socket()         # Create a socket object

        self.s.bind(("0.0.0.0", 8091))        # Bind to the port
        self.s.listen(5)                 # Now wait for client connection.

    def update_socket(self, i, socket):
        if i == 1:
            self.dashboard_socket = socket
        if i == 2:
            self.vision_socket = socket
        if i == 3:
            self.hero_socket = socket

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
                if t == 250:
                    print("Recieved Indetification Packet")
                    i = msg[1]
                    self.update_socket(i, clientsocket)
                elif t == 1 or t == 2 or t == 9:
                    print("Recieved Data for Hero")
                    if self.hero_socket != None:
                        self.hero_socket.send(msg)
                    else:
                        print("Hero is not connected")
                else:
                    print("Invalid type: ", t)
        finally:
            clientsocket.close()
            self.update_socket(i, None)
    
    def run(self):
        while True:
            c, addr = self.s.accept()     # Establish connection with client.
            print("Got connection from ", addr)
            t = threading.Thread(target=self.on_new_client,args=(c,addr))
            t.start()
        self.s.close()


s = SimpleRouter()
s.run()
