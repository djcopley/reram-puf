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


class ClientManager:

    def __init__(self):
        """Constructor method."""
        # JSON data to be held by client manager
        self.clients = {}

    def create_client(self, user: str, passwd: str, salt: bytes) -> dict:
        """Create a client object with client attributes."""
        client = {}
        client[user] = {}
        client[user]["key"] = passwd
        client[user]["salt"] = salt
        return client

    def load_client(self, user: str) -> dict:
        """"Load a client's data for authentication."""
        try:
            client = self.clients[user]
        except KeyError:
            print(f"[ERROR]: Client username {user} does not exist.")
            client = None
        finally:
            return client

    def save_client(self, client: dict) -> bool:
        """Save a client's data to the client JSON database."""
        # May add functionality later to control overwriting existing users
        self.clients.update(client)
        return True
