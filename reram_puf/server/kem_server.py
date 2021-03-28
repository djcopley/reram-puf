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
from client_manager import ClientManager
from cryptography import Cryptography

"""KEM Server Class for creating a server instance for communication."""


class KEMServer:

    def __init__(self):
        """Constructor method."""
        self.SALT_LEN = 16
        self._database = ClientManager()
        self._crypto_suite = Cryptography()
        self._current_list = [700, 600, 500, 400]
        self._addresses = []
        self._orders = []


    def enrollment(self) -> bool:
        """Conduct enrollment for a new client."""
        #Add functionality later to prevent duplicate users
        user = input("Enter username: ")

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
            return False
        
        salt = self._crypto_suite.generate_salt(self.SALT_LEN)
        pwd_hash = self._crypto_suite.hash(password1, salt)
        new_client = self._database.create_client(user, pwd_hash, salt)
        self._database.save_client(new_client)
        client_lut = input("Enter LUT: ") #May change to recv LUT from client
        self._database.save_lookup_table(user, client_lut)
        return True

    
    def authenticate(self, user: str) -> bool:
        """Authenticate an existing client."""
        try:
            info = self._database.clients[user]
            salt = info["salt"]
            key = info["key"]
            print(f"User : {user}")
            passwd = getpass.getpass(prompt="Enter Password:")
            yield passwd
            pwd_hash = self._crypto_suite.hash(passwd, salt)
            if pwd_hash == key:
                print("[SUCCESS]: Authentication Successful.")
                yield True
            else:
                print("[ERROR]: Authentication failed. Invalid username or password.")
                yield False
        except:
            print("[ERROR]: Authentication failed. User does not exist.")
            yield False


    def handshake(self, client: str) -> bool:
        """Conduct handshake to begin a client connection."""
        [passwd, auth] = self.authenticate(client)
        if auth:
            rand_num = self._crypto_suite.generate_salt(self.SALT_LEN)
            #TODO: Send number to client
            instructions = self._crypto_suite.hash(passwd, rand_num)
            #TODO: Parse for addresses and orders (use some .split here?)
            #TODO: store the list of addresses and list of orders
            return True
        return False
            


    def get_new_message(self) -> str:
        """Get a new message to be encrypted and transmitted."""
        msg = input("Enter message to send: ")
        return msg


    def encrypt_message(self, user: str, msg: str, group_len: int) -> bytes:
        """Conduct encryption process steps on a new message string."""
        voltage_groups = []
        binary_msg = self._convert_plaintext_to_binary(msg)
        binary_groups = self._group_binary_string(binary_msg, group_len)
        for group in binary_groups:
            addr = self._get_next_address()
            if addr is None:
                return None
            current = self._current_lookup(group)
            voltage = self._voltage_lookup(user, current, addr)
            voltage_groups.append(voltage)
        ciphertext = struct.pack(f"{len(voltage_groups)}f", *voltage_groups)
        #maybe clear addresses and orders before next message?
        return ciphertext      


    def decrypt_message(self):
        """Conduct decryption process steps on an incoming ciphertext."""
        pass


    def _convert_plaintext_to_binary(self, string: str) -> str:
        """Convert a plaintext string to a binary string."""
        binary_str = ""
        for char in string:
            binary_int = ord(char)
            binary_char = format(binary_int, '08b')
            binary_str += binary_char
        return binary_str


    def _group_binary_string(self, binary_msg: str, group_len: int) -> list:
        """Group a binary string into clusters of group length.
        If string length is not a multiple of group length, pad front with
        zeros."""
        string = binary_msg
        string_list = []
        while len(string) % group_len != 0:
            string = "0" + string
        for index in range(0,len(string),2):
            string_list.append(string[index:index+group_len])
        return string_list


    def _get_next_address(self) -> int:
        """Return the next address to use for lookup table as integer."""
        try:
            next_order = self._orders.pop(0)
            self._orders.append(next_order)
            addr = int(self._addresses[next_order], 2)
        except IndexError:
            print(f"[ERROR]: Failed to fetch address. Bad addresses/orders.")
            addr = None
        finally:    
            return addr


    def _current_lookup(self, code: str) -> int:
        """Convert from binary code to current using current lookup."""
        index = int(code, 2)
        try:
            current = self._current_list[index]
        except IndexError:
            print(f"[ERROR]: Invalid binary code {code} for current lookup.")
            current = None
        finally:
            return current


    def _voltage_lookup(self, user: str, current: int, addr: int) -> float:
        """Perform voltage lookup given current and cell address."""
        try:
            lut = self._database.clients["user"]["image"]
            voltage = lut[current][addr]
        except KeyError:
            print(KeyError)
            print(f"[ERROR]: Invalid key in voltage lookup.")
            voltage = None
        finally:
            return voltage
