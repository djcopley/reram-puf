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

"""Message utilities to be used as an encryption/decryption interface."""


def convert_plaintext_to_binary(string: str) -> str:
    """Convert a plaintext string to a binary string."""
    binary_str = ""
    for char in string:
        binary_int = ord(char)
        binary_char = format(binary_int, '08b')
        binary_str += binary_char
    return binary_str

def group_binary_string(binary_msg: str, group_len: int) -> list:
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
