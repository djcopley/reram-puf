import struct
import serial
import time


def enroll():
    currents = {
        400: "0110010000",
        300: "0100101100",
        200: "0011001000",
        100: "0001100100" }
    addresses = ["00","01","10","11"]
    lut = {
        400 : [],
        300 : [],
        200 : [],
        100 : [] }

    for key, value in currents.items():
        for addr in addresses:
            msg = "0001"
            msg += addr + value
            print(f"MSG: {msg}")
            msg_bytes = f"<{msg}>".encode("utf-8")
            device.write(msg_bytes)
            print("Waiting for response...")
            #time.sleep(25)
            read = device.read(6)
            out = read.decode("utf-8").split("\r\n")
            print("Response: {}".format(out))
            out = read.decode("utf-8").split("\r\n")[0]
            out = float(out)
            print(f"output: {out}")
            lut[key].append(out)
    return lut


device = serial.Serial(port="COM4", baudrate=115200)
#device.timeout = 2
device.flushInput()
device.flushOutput()
time.sleep(2)
lut = enroll()
print(lut)




"""
while True:
    msg = input("Enter binary input to Arduino Serial: ")
    msg_int = int(msg, 2)
    msg_bytes = f"<{msg}>".encode("utf-8")
    device.write(msg_bytes)
    print("Waiting for response...")
    time.sleep(0.5)
    read = device.read_all()
    out = read.decode("utf-8").split("\r\n")
    print("Response: {}".format(out))
    out = read.decode("utf-8").split("\r\n")[0]
    out = float(out)
    print(f"output: {out}")
    #print("Value converted to float: {}".format(struct.unpack("f", read)))
"""