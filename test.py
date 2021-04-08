import struct
import serial


device = serial.Serial(port="COM4", baudrate=115200)

while True:
    byte = int(input("Enter byte to write (binary): "), 2)
    device.write(byte)

    print("Waiting for response...")
    read = device.read(4)
    print("Response: {}".format(read))
    print("Value converted to float: {}".format(struct.unpack("f", read)))
