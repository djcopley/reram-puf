import serial
import struct
import hashlib

from getpass import getpass


class Client:
    def __init__(self, port="/dev/tty.usbmodem14101", baudrate=115200):
        self.device = serial.Serial(port=port, baudrate=baudrate)
        self.orders = []
        self.addresses = (0, 1, 2, 3)

    def handshake(self):
        # Get password
        password = getpass()
        # Send password to server
        # Get salt
        salt = b""
        # Hash the password with the salt
        hashed_pw = self.sha_hash(password, salt)
        # Generate instructions

    @staticmethod
    def sha_hash(password: str, salt: bytes) -> str:
        """
        Calculated SHA-256 hash

        :param password:
        :param salt:
        :return:
        """
        digest = hashlib.sha256()
        msg = bytes(password, "utf-8") + salt
        digest.update(msg)
        return digest.hexdigest()

    def decrypt(self, cipher):
        plain = ""
        return plain

    def puf_instr(self, addr: int, voltage: float):
        """
        Issue and instruction to the PUF and read back the calculated current

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
