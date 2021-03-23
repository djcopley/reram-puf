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

"""KEM Server Class for creating a server instance for communication."""


class KEMServer:

    def __init__(self):
        """Constructor method."""
        pass

    def enrollment(self):
        """Conduct enrollment for a new client."""
        pass

    def handshake(self):
        """Conduct handshake to begin a client connection."""
        pass

    def new_message(self):
        """Generate a new encrypted message to be transmitted."""

    def encrypt_message(self):
        """Conduct encryption process steps on a new message string."""
        pass

    def decrypt_message(self):
        """Conduct decryption process steps on an incoming ciphertext."""
        pass

    def generate_salt(self):
        """Generate a new salt for handshake or enrollment."""
        pass
