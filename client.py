import serial
import struct
import hashlib
import getpass


class Client:
    def __init__(self, port="/dev/tty.usbmodem14101", baudrate=115200):
        self.device = serial.Serial(port=port, baudrate=baudrate)
        self.device.readline()  # Flush message queue

    def decrypt(self, cipher):
        plain = ""
        return plain

    def puf_instr(self, addr, voltage):
        pass

    def get_current(self):
        struct.unpack(self.device.read(4))


if __name__ == '__main__':
    port = input("Enter port: ")
    client = Client(port=port)
