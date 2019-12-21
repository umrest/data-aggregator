# Test the role of hero

import serial

with serial.Serial('/tmp/ttyV11', 115200, timeout=1) as ser:
    while True:
        if(ser.in_waiting >= 128 + 3):
            key0 = ser.read()[0]
            while key0 != 44:
                print("out of sync")
                if(ser.in_waiting < 1):
                    continue
                key0 = ser.read()[0]
            key1 = ser.read()[0]
            key2 = ser.read()[0]
            if(key1 != 254 or key2 != 153):
                continue
            else:
                buf = ser.read(128)
                #print(buf[0])

                if(buf[0] == 2):
                    print("V", end=" ")
                elif(buf[0] == 9):
                    print("D", end=" ")
                elif(buf[0] == 1):
                    print("J", end=" ")
                else:
                    print("invalid type")
        
