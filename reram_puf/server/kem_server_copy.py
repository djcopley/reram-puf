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

"""KEM Server Class for creating a server instance for communication."""


class KEMServer:

    def __init__(self, salt_len=16, group_len=2):
        """Constructor method."""
        self.salt_len = salt_len
        self.group_len = group_len
        self._addresses = []
        self._orders = []

    def authenticate(self, client: dict) -> Generator[str,bool]:
        """Authenticate a user with client data."""
        passwd = getpass.getpass()
        yield passwd

        pwd_hash = self.hash(passwd, client["salt"])
        if pwd_hash == client["key"]:
            print("[SUCCESS]: Authentication Successful")
            yield True
        else:
            print("[ERROR]: Authentication failed. Invalid username or password.")
            yield False

    def enroll(self) -> bool:
        """Enroll a new client."""
        pass