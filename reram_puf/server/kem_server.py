######## Key Encapsulation Mechanism (KEM) Server Utilities ########
#
# Authors: Corey Cline
#          Daniel Copley
#
# Date: 03/22/2021
#
# Description:
# A KEM Server Class to be used as an interface to all of the server utilities
# required for communication with a client. This includes the enrollment with a
# new client, the handshake process, and the sending and receiving of messages.
# Messages will be encrypted/decrypted with KEM, and all necessary data for
# remembering client enrollments, including the Voltage Lookup Table (VLT),
# will be stored here.
#
################################################################################
import os
import struct
import getpass
import hashlib
from reram_puf.common.string_manager import *
from reram_puf.server.client_manager import *

"""KEM Server Class for creating a server instance for communication."""


class KEMServer:

    def __init__(self, salt_len=16, group_len=2):
        """Constructor method."""
        self.salt_len = salt_len
        self.group_len = group_len
        self.addresses = []
        self.clients = {}
        self.current_list = [400, 300, 200, 100]
        self.orders = []
        self.salt = b""

    def authenticate(self, user: str, passwd=None) -> list:
        """Authenticate a user with client data."""
        # Fetch client data from database and check for none
        client = load_client(user, self.clients)
        if client is None:
            return None, None
        # Get password if not specified, yield the password back
        if passwd is None:
            passwd = getpass.getpass()
        # Hash password and check against client data, yield auth result
        pwd_hash = self.hash(passwd, client["salt"])
        if pwd_hash == client["key"]:
            # print("[SUCCESS]: Authentication Successful")
            return passwd, True
        else:
            # print("[ERROR]: Authentication failed. Invalid username or password.")
            return passwd, False

    def close(self):
        """Close a client connection."""
        self.addresses = []
        self.orders = []
        self.salt = b""

    def current_lookup(self, code: str) -> int:
        """Convert from binary code to current using current lookup."""
        index = int(code, 2)
        try:
            current = self.current_list[index]
        except IndexError:
            print(f"[ERROR]: Invalid binary code {code} for current lookup.")
            current = None
        finally:
            return current

    def decrypt_message(self, user: str, msg: bytes) -> str:
        """Decrypt a messags sent from a client."""
        binary_msg = ""
        for index in range(0, len(msg), 4):
            addr = self.get_next_address()
            byte_group = msg[index:index + 4]
            voltage = round(struct.unpack("f", byte_group)[0], 2)
            current = self.reverse_voltage_lookup(user, voltage, addr)
            if current is None:
                return None
            binary_group = self.reverse_current_lookup(current, self.group_len)
            if binary_group is None:
                return None
            binary_msg += binary_group
        plaintext = convert_binary_to_plaintext(binary_msg)
        return plaintext

    def encrypt_message(self, user: str, msg: str) -> bytes:
        """Encrypt a message string to send to client."""
        # Set voltage stream and chunk message into binary groups
        voltages = []
        binary_msg = convert_plaintext_to_binary(msg)
        binary_groups = group_binary_string(binary_msg, self.group_len)
        # Convert from binary group to voltage value from Lookup Tables
        for group in binary_groups:
            addr = self.get_next_address()
            if addr is None:
                return None
            current = self.current_lookup(group)
            voltage = self.voltage_lookup(user, current, addr)
            voltages.append(voltage)
        print(f"VOLTAGE STREAM: {voltages}")
        # Convert from voltage list of floats to byte stream
        ciphertext = struct.pack(f"{len(voltages)}f", *voltages)
        return ciphertext

    def enroll(self, user=None, passwd=None, salt=None, lut=None) -> bool:
        """Enroll a new client."""
        # Get username if not specified
        if user is None:
            user = input("Enter username: ")
        # Get password if not specified. Give 3 tries to confirm password
        if passwd is None:
            pass_confirmed = False
            strikes = 0
            while not pass_confirmed and strikes < 3:
                password1 = getpass.getpass(prompt="Enter Password:")
                password2 = getpass.getpass(prompt="Confirm Password:")
                if password1 == password2:
                    pass_confirmed = True
                else:
                    print("[ERROR]: Passwords do not match.")
                    strikes += 1
            if strikes == 3:
                print("[ERROR]: Password attemps exceeded.")
                return False
        # Generate salt if not specified and hash password for storage
        if salt is None:
            salt = self.generate_salt(self.salt_len)
        pwd_hash = self.hash(passwd, salt)
        # Get LUT if not specified
        if lut is None:
            lut = input("Enter Client Lookup Table: ")
        # Create client object and save to database
        new_client = create_client(user, pwd_hash, salt, lut)
        return save_client(new_client, self.clients)

    def generate_salt(self, length: int) -> bytes:
        """Generate a new salt for handshake or enrollment."""
        return os.urandom(length)

    def get_next_address(self) -> int:
        """Return the next address to use for lookup table as integer."""
        try:
            next_order = self.orders.pop(0)
            self.orders.append(next_order)
            addr = int(self.addresses[next_order], 2)
        except IndexError:
            print(f"[ERROR]: Failed to fetch address. Bad addresses/orders.")
            addr = None
        finally:
            return addr

    def handshake(self, user: str, passwd=None, rand=None) -> bool:
        """Handshake process with a client."""
        passwd, auth = self.authenticate(user, passwd=passwd)
        if auth:
            if rand is None:
                rand = self.generate_salt(self.group_len)
                self.salt = rand
            print(f"[HANDSHAKE]: {rand}")
            pwd_hash = self.hash(passwd, rand)
            # Orders is first half of hash as grouped binary string integers
            orders = pwd_hash[:len(pwd_hash) // 2]
            orders = bin(int(orders, 16))[2:]
            orders = group_binary_string(orders, self.group_len)
            orders = [int(num, 2) for num in orders]
            # Set the addresses and orders for the session (until close)
            self.addresses = ["00", "01", "10", "11"]
            self.orders = orders
            print(f"ORDERS: {self.orders}")
            return True
        print("[HANDSHAKE]: Failed.")
        return False

    def hash(self, message: str, salt: bytes) -> str:
        """Conduct SHA-256 Hash on message with salt."""
        digest = hashlib.sha256()
        msg = bytes(message, "utf-8") + salt
        digest.update(msg)
        return digest.hexdigest()

    def reverse_current_lookup(self, current: int, group_len: int) -> str:
        """Retrieve the binary code N given the current."""
        if current in self.current_list:
            code = self.current_list.index(current)
            code = format(code, f"0{group_len}b")
            return code
        print("[ERROR]: Current not found in current list.")
        return None

    def reverse_voltage_lookup(self, user: str, voltage: float,
                               addr: int) -> int:
        """Retrieve the current given user, voltage, and address."""
        try:
            lut = self.clients["user"]["image"]
            lut_keys = list(lut.keys())
            lut_vals = list(lut.values())
            for index in range(0, len(lut_vals)):
                if lut_vals[index][addr] == voltage:
                    current = lut_keys[index]
                    return current
            print("[ERROR]: Voltage not found in lookup table.")
            return None
        except KeyError:
            print(f"[ERROR]: User {user} does not exist.")
            return None

    def voltage_lookup(self, user: str, current: int, addr: int) -> float:
        """Perform voltage lookup given current and cell address."""
        voltage = None

        try:
            voltage = self.clients[user]["image"][current][addr]
        except KeyError:
            print(KeyError)
            print(f"[ERROR]: Invalid key(s) {current},{addr} in voltage lookup.")
        finally:
            return voltage
