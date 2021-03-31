######## Client Manager Utilities ########
#
# Authors: Corey Cline
#          Daniel Copley
#
# Date: 03/22/2021
#
# Description:
# A set of supporting methods for modifying data in a JSON database.
#
################################################################################
import json

"""JSON utilities to be used as a JSON Client Database interface."""

def create_client( user: str, passwd: str, salt: bytes, lut: dict) -> dict:
    """Create a client object with client attributes."""
    client = {}
    client[user] = {}
    client[user]["key"] = passwd
    client[user]["salt"] = salt
    client[user]["image"] = lut
    return client

def load_client(user: str, database: dict) -> dict:
    """"Load a client's data for authentication."""
    try:
        client = database[user]
    except KeyError:
        print(f"[ERROR]: Client username {user} does not exist.")
        client = None
    finally:
        return client

def save_client(client: dict, database: dict) -> bool:
    """Save a client's data to the client JSON database."""
    try:
        user = list(client.keys())[0]
        if user in database:
            print(f"[ERROR]: Client username {user} already exists.")
            return False
    except KeyError:
        print(f"[ERROR]: Key Error when searching for user.")
        return False

    database.update(client)
    return True
