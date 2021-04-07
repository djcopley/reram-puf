import serial
import struct
import hashlib

from getpass import getpass
from reram_puf.common.string_manager import group_binary_string, convert_binary_to_plaintext


class Client:
    def __init__(self, port="/dev/tty.usbmodem14101", baudrate=115200):
        self.device = serial.Serial(port=port, baudrate=baudrate)
        self.group_len = 2
        self.orders = None
        self.addresses = (0, 1, 2, 3)
        self.current_list = (700, 600, 500, 400)

    def close(self):
        """Close the current connection."""
        self.orders = None

    def handshake(self, passwd: str, salt: bytes):
        """Conduct handshake with server."""
        # Hash the password with the salt
        hashed_pw = self.sha_hash(passwd, salt)
        # Generate instructions
        self.orders = hashed_pw[:len(hashed_pw) // 2]
        self.orders = bin(int(self.orders, 16))[2:]
        self.orders = group_binary_string(self.orders, self.group_len)

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
        binary_message = ""

        for index in range(0, len(cipher), 4):
            addr = self.get_next_address()
            byte_group = cipher[index:index + 4]
            voltage = struct.unpack("f", byte_group)[0]
            current = self.puf_instr(addr, voltage)
            binary_group = self.current_lookup(current, self.group_len)
            binary_message += binary_group

        plain_text = convert_binary_to_plaintext(binary_message)

        return plain_text

    def current_lookup(self, current, group_len: int) -> str:
        """Retrieve the binary code N given the current."""
        smallest_difference = abs(self.current_list[0] - current)
        code = format(0, f"0{group_len}b")

        for stored_current, index in enumerate(self.current_list)[1:]:
            if abs(current - stored_current) < smallest_difference:
                smallest_difference = stored_current
                code = format(index, f"0{group_len}b")

        return code

    def get_next_address(self):
        """Return the next address to use for lookup table as integer."""
        try:
            next_order = self.orders.pop(0)
            self.orders.append(next_order)
            addr = int(self.addresses[next_order], 2)
            return addr
        except IndexError:
            print(f"[ERROR]: Failed to fetch address. Bad addresses/orders.")

    def puf_instr(self, addr: int, voltage: float):
        """
        Issue and instruction to the PUF and read back the calculated current

        :param addr: ReRam cell address (0-3)
        :param voltage: Floating point voltage (0-5v)
        :return: Calculated current
        """
        # Convert voltage to 6bit voltage
        voltage = round(voltage * 64 / 5) & 0b00111111
        self.device.write(addr << 6 | voltage)
        res, = struct.unpack("f", self.device.read(4))
        return res


if __name__ == '__main__':
    # port = input("Enter port: ")
    client = Client()
    print(client.puf_instr(00, 3.1))
