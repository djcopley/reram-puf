######## Client Database Utilities ########
#
# Authors: Corey Cline
#          Daniel Copley
#
# Date: 03/22/2021
#
# Description:
# A Client Database Class used to store and modify client credentials in a
# JSON database. Will conduct file I/O to the client database for saving new
# clients and loading existing clients.
#
################################################################################
import json

"""JSON Clients Class to be used as a JSON Client Database interface."""


class JSON_Clients:

    def __init__(self):
        """Constructor method."""
        pass

    def create_client(self, user: str, passwd: str, salt: bytes) -> dict:
        """Create a client object with client attributes."""
        pass

    def load_client(self, user: str) -> dict:
        """"Load a client's data for authentication."""
        pass

    def save_client(self, user: str, key: str, salt: bytes) -> bool:
        """Save a client's data to the client JSON database."""
        pass
