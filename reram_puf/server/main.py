import argparse
import logging

from reram_puf import __version__
from reram_puf.common.network import Network
from reram_puf.common.mqtt_client import MQTTClient

# Define callback function for MQTT message callback
def on_message( client, userdata, message ):
    """Callback function for receiving messages."""
    msg = message.payload.decode( "utf-8" )
    # Capture the message in the global Network Class queue
    network.mqtt.msg_queue.append( msg )

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", 
        version=__version__)
    parser.add_argument("--host", type=str, required=True,
        help="Hostname to connect to for network communication.")
    parser.add_argument("--client", type=str, required=True,
        help="Name of the client who is connecting to the network.")
    return parser.parse_args()

def main():
    args = parse_args()
    global network # Declare global for on_message to access the queue
    network = Network(args.host, args.client)
    network.mqtt.client.on_message = on_message
    network.connect()
    incoming = network.receive("server/receive")
    print(f"Incoming: {incoming}")
    network.disconnect()



if __name__ == '__main__':
    main()
