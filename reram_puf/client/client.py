import serial
import struct
import hashlib

from reram_puf.common.string_manager import *
from reram_puf.common.network import Network
from getpass import getpass


class Client:
    def __init__(self, port: str, baudrate: int):
        self.device = serial.Serial(port=port, baudrate=baudrate)
        self.orders = []

    def hash(self, message: str, salt: bytes) -> str:
        """Conduct SHA-256 Hash on message with salt."""
        digest = hashlib.sha256()
        msg = bytes(message, "utf-8") + salt
        digest.update(msg)
        return digest.hexdigest()

    def handshake(self):
        password = getpass()
        # Send password
        # Get salt
        salt = b""
        hash = self.hash(password, salt)
        self.orders = hash[:len(hash) // 2]

    def get_message(self):
        # Get message from MQTT broker (blocking operation)
        return

    def decrypt_message(self, message):
        binary_msg = ""
        for index in range(0, len(message), 4):
            addr = self.get_next_address()
            byte_group = message[index:index + 4]
            voltage = round(struct.unpack("f", byte_group)[0], 2)
            current = self.get_current(voltage, addr)
            if current is None:
                return None
            binary_group = self.reverse_current_lookup(current, self.group_len)
            if binary_group is None:
                return None
            binary_msg += binary_group
        plaintext = convert_binary_to_plaintext(binary_msg)
        return plaintext

    def get_current(self, voltage, addr):
        return

    def run(self):
        self.handshake()
        while True:
            cipher_text = self.get_message()
            plain_text = self.decrypt_message(cipher_text)
            print("Message Recieved!: {}".format(plain_text))
