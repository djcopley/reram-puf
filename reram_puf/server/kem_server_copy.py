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

"""KEM Server Class for creating a server instance for communication."""


class KEMServer:

    def __init__(self, salt_len=16, group_len=2):
        """Constructor method."""
        self.salt_len = salt_len
        self.group_len = group_len
        self._addresses = []
        self._orders = []

    def authenticate(self, user: dict, passwd=None) -> list:
        """Authenticate a user with client data."""
        if passwd is None:
            passwd = getpass.getpass()
        yield passwd

        pwd_hash = self.hash(passwd, user["salt"])
        if pwd_hash == user["key"]:
            print("[SUCCESS]: Authentication Successful")
            yield True
        else:
            print("[ERROR]: Authentication failed. Invalid username or password.")
            yield False

    def enroll(self, user=None, passwd=None, salt=None) -> tuple:
        """Enroll a new client."""
        if user is None:
            user = input("Enter username: ")

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
                return None
        if salt is None:
            salt = self.generate_salt(self.salt_len)
        pwd_hash = self.hash(passwd, salt)
        return user, pwd_hash, salt

    def generate_salt(self, length: int) -> bytes:
        """Generate a new salt for handshake or enrollment."""
        return os.urandom(length)

    def handshake(self, user: dict, passwd=None) -> bytes:
        """Handshake process with a client."""
        [passwd, auth] = self.authenticate(user, passwd=passwd)
        if auth:
            rand = self.generate_salt(self.group_len)
            print(f"[HANDSHAKE]: {rand}")
            return rand
        print("[HANDSHAKE]: Failed.")
        return None

    def hash(self, message: str, salt: bytes) -> str:
        """Conduct SHA-256 Hash on message with salt."""
        digest = hashlib.sha256()
        msg = bytes(message, "utf-8") + salt
        digest.update(msg)
        return digest.hexdigest()
