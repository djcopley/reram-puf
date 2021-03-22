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
import hashlib
import getpass

"""Hash Algorithms Class to be used as a Hash interface."""


class Cryptography:

    def __init__(self):
        """Constructor method."""
        pass

    def enroll(self):
        """Enroll a new client."""
        pass

    def authenticate(self) -> bool:
        """Authenticate an existing client."""
        pass

    def hash(self, algorithm: str, password: str, salt: bytes) -> str:
        """Conduct hash based on specified algorithm, password, and salt."""
        pass
