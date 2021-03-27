# SCRIPT USED ONLY FOR TESTING. 
# DON'T KEEP ANYTHING IMPORTANT HERE.

import logging
from kem_server import KEMServer

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

ks = KEMServer()

# Create client in server database
client = ks.database.create_client("user", "password", b"salt")
logging.info(f"Client info: {client}")
if ks.database.save_client(client):
    logging.info(f"Client saved: {ks.database.clients['user']}")

# Create Voltage LUT and save to client
LUT = {
    700 : [2.8,3.5,4.2,4.9], 
    600 : [2.4,3.0,3.6,4.2],
    500 : [2.0,2.5,3.0,3.5],
    400 : [1.6,2.0,2.4,2.8] }
if ks.database.save_lookup_table("user", LUT):
    logging.info(f"LUT Saved: {ks.database.clients['user']['image']}")

# Handshake
addresses = b"00011011"
orders = b"4321"
address_groups = ks._group_binary_string(addresses, 2)
logging.info(f"Addresses: {address_groups}")
orders = [ int(char) for char in orders ]
logging.info(f"Order of addresses: {orders}")

# Get message
message = "HI"
logging.info(f"Plaintext message: {message}")

# Convert to binary string
bin = ks._convert_plaintext_to_binary(message)
logging.info(f"Binary string:     {bin}")

# Group binary string by 2
bin_groups = ks._group_binary_string(bin, 2)
logging.info(f"Binary groupings:  {bin_groups}")

# Perform current lookup
current_groups = []
for group in bin_groups:
    current = ks._current_lookup(group)
    current_groups.append(current)
logging.info(f"Current stream:    {current_groups}")

# Perform voltage lookup
voltage_groups = []
for current in current_groups:
    voltage = ks._voltage_lookup("user", current, 0)
    voltage_groups.append(voltage)
logging.info(f"Voltage stream: {voltage_groups}")
