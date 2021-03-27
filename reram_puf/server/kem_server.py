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
from client_manager import ClientManager

"""KEM Server Class for creating a server instance for communication."""


class KEMServer:

    def __init__(self):
        """Constructor method."""
        self.database = ClientManager()
        self._current_list = [700, 600, 500, 400]
        pass

    def enrollment(self):
        """Conduct enrollment for a new client."""
        pass

    def handshake(self, client: str):
        """Conduct handshake to begin a client connection."""
        #TODO: Generate a random number
        #TODO: Send number to client
        #TODO: Hash number with client's password
        #TODO: Parse for addresses and orders
        #TODO: return the list of addresses and list of orders
        pass

    def get_new_message(self) -> str:
        """Get a new message to be encrypted and transmitted."""
        msg = input("Enter message to send: ")
        return msg

    def encrypt_message(self, msg: str, group_len: int) -> bytes:
        """Conduct encryption process steps on a new message string."""
        voltage_groups = []
        binary_msg = self._convert_plaintext_to_binary(msg)
        binary_groups = self._group_binary_string(binary_msg)
        for group in binary_groups:
            current = self._current_lookup(group, group_len)
            

    def decrypt_message(self):
        """Conduct decryption process steps on an incoming ciphertext."""
        pass

    def generate_salt(self):
        """Generate a new salt for handshake or enrollment."""
        pass

    def _create_lookup_table(self, voltages: list) -> dict:
        """Create voltage lookup table from 2D array of voltages."""
        lut = {}
        # May not need this, as the arduino should create lut from array
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
            lut = self.database.clients["user"]["image"]
            voltage = lut[current][addr]
        except KeyError:
            print(KeyError)
            print(f"[ERROR]: Invalid key in voltage lookup.")
            voltage = None
        finally:
            return voltage
