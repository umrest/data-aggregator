import serial

with serial.Serial('COM12', 115200, parity=serial.PARITY_EVEN) as ser:
    while True:
        data = ser.read(128)
        print("TYPE: ", data[0], " BUTTONs1: ", data[1])