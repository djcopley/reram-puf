import argparse

from reram_puf import __version__
from reram_puf.common.network import Network
from reram_puf.common.mqtt_client import MQTTClient

# Define callback function for MQTT message callback
def on_message( client, userdata, message ):
    """Callback function for receiving messages."""
    msg = message.payload.decode( "utf-8" )
    client.msg_queue.append( msg )
    logging.info( "\n\tTopic: {}\n\tMessage: {}\n\tRetained: {}".format(
                  message.topic,msg, message.retain ) )

    if ( message.retain == 1 ):
        logging.info( "This was a retained message." )

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
    network = Network(args.host, args.client)
    network.connect()
    msg = "Hello from Network"
    network.send("test", msg)

    msg_2 = "Hello from MQTTClient"
    client = MQTTClient("192.168.0.2", "kem_server")
    client.client.on_message = on_message
    client.connect()
    client.loop_start()
    client.publish("test", msg_2, qos=2, retain=False)


if __name__ == '__main__':
    main()
