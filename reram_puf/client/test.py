import struct
import serial
import time


device = serial.Serial(port="COM4", baudrate=115200)
device.read()

while True:
    byte = int(input("Enter byte to write (binary): "), 2).to_bytes(1, "big")
    device.write(byte)
    print("Waiting for response...")
    #time.sleep(0.5)
    read = device.read()
    print("Response: {}".format(read))
    #print("Value converted to float: {}".format(struct.unpack("f", read)))
