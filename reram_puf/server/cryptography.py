######## Cryptography Utilities ########
#
# Authors: Corey Cline
#          Daniel Copley
#
# Date: 03/22/2021
#
# Description:
# A Cryptography Class to be used for providing an interface for hashing data 
# with a variety of hash algorithms, as well as accessing client credentials,
# enrolling new clients, and authenticating existing clients. Will access a
# clients JSON database for enrolling and authenticating clients. 
#
###############################################################################
import os
import hashlib
import getpass

"""Hash Algorithms Class to be used as a Hash interface."""


class Cryptography:

    def __init__(self):
        """Constructor method."""
        self.SALT_LEN = 16

    def hash(self, password: str, salt: bytes) -> str:
        """Conduct hash based on specified algorithm, password, and salt."""
        digest = hashlib.sha256()
        msg = bytes(password, "utf-8") + salt
        digest.update(msg)
        return digest.hexdigest()

    def generate_salt(self, length: int) -> bytes:
        """Generate a new salt for handshake or enrollment."""
        return os.urandom(length)
