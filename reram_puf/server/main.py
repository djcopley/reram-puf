import argparse
import logging

from reram_puf import __version__
from reram_puf.common.network import Network
from reram_puf.common.mqtt_client import MQTTClient
from reram_puf.server.kem_server import KEMServer


# Define callback function for MQTT message callback
def on_message(client, userdata, message):
    """Callback function for receiving messages."""
    msg = message.payload.decode("utf-8")
    # Capture the message in the global Network Class queue
    network.mqtt.msg_queue.append(msg)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", 
        version=__version__)
    parser.add_argument("--host", type=str, required=True,
        help="Hostname to connect to for network communication.")
    parser.add_argument("--client", type=str, required=True,
        help="Name of the client who is connecting to the network.")
    parser.add_argument("--log", type=str, default="INFO", 
        help="Specify log level for main program.")
    return parser.parse_args()


def log_config(log_level):
    # Initialize the program logger
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid Log Level: {log_level}")
    logging.basicConfig(level=numeric_level, 
        format="%(levelname)s: %(message)s")


def main():
    # Parse args and set log
    args = parse_args()
    log_config(args.log)

    # Declare global network for on_message to access the message queue
    global network
    network = Network(args.host, args.client)
    network.mqtt.client.on_message = on_message
    logging.debug("Connecting to Network...")
    network.connect()
    logging.debug("Connected to MQTT Broker.")
    
    # Create server and wait for enrollment message
    server = KEMServer(salt_len=16, group_len=2)
    enrollment_data = network.receive("enrollment")
    user, passwd, salt, lut = enrollment_data.split(",")
    if not salt:
        salt = None

    # Enroll new user, conduct handshake, send a message
    if server.enroll(user=user, passwd=passwd, salt=salt, lut=lut):
        if server.handshake(user, passwd=passwd):
            network.send("handshake", sever.salt)
            message = input("Enter message: ")
            logging.debug(f"Message to be sent: {message}")
            ciphertext = server.encrypt_message(user, message)
            logging.debug(f"Encrypted message: {ciphertext}")
            network.send(user, ciphertext)
        logging.debug("Closing client connection...")
        server.close()
    logging.debug("Disconnecting from broker...")
    network.disconnect()


if __name__ == '__main__':
    main()
