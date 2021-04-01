import serial
import struct
import hashlib
import getpass


class Client:
    def __init__(self, port="/dev/tty.usbmodem14101", baudrate=115200):
        self.device = serial.Serial(port=port, baudrate=baudrate)

    def decrypt(self, cipher):
        plain = ""
        return plain

    def puf_instr(self, addr: int, voltage: float):
        """

        :param addr: ReRam cell address (0-3)
        :param voltage: Floating point voltage (0-5v)
        :return: Calculated current
        """
        # Conver voltage to 6bit voltage
        voltage = round(voltage * 64 / 5) & 0b00111111
        self.device.write(addr << 6 | voltage)
        res, = struct.unpack("f", self.device.read(4))
        return res


if __name__ == '__main__':
    # port = input("Enter port: ")
    client = Client()
    print(client.puf_instr(00, 3.1))
