# SCRIPT USED ONLY FOR TESTING. 
# DON'T KEEP ANYTHING IMPORTANT HERE.

import logging
from kem_server import KEMServer

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

ks = KEMServer()

message = "HI"
logging.info(f"Plaintext message: {message}")

bin = ks._convert_plaintext_to_binary(message)
logging.info(f"Binary string:     {bin}")

bin_groups = ks._group_binary_string(bin, 2)
logging.info(f"Binary groupings:  {bin_groups}")

current_groups = []
for group in bin_groups:
    current = ks._current_lookup(group)
    current_groups.append(current)
logging.info(f"Current stream:    {current_groups}")


