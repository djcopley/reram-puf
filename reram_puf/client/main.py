import argparse

from getpass import getpass

from reram_puf.common.network import Network
from reram_puf import __version__
from reram_puf.client.client import Client


# Define callback function for MQTT message callback
def on_message(client, userdata, message):
    """Callback function for receiving messages."""
    msg = message.payload.decode("utf-8")
    # Capture the message in the global Network Class queue
    network.mqtt.msg_queue.append(msg)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__
    )
    parser.add_argument("serial_port",
                        type=str,
                        help="the serial port of arduino puf")

    parser.add_argument("baud_rate",
                        type=str,
                        help="the arduino serial baud rate")

    parser.add_argument("--host", type=str, required=True,
                        help="Hostname to connect to for network communication.")

    parser.add_argument("--client", type=str, required=True,
                        help="Name of the client who is connecting to the network.")

    return parser.parse_args()


def main():
    args = parse_args()
    client = Client(port=args.serial_port, baudrate=args.baud_rate)

    global network
    network = Network(args.host, args.client)
    network.connect()

    username = input("Please enter username: ")
    password = getpass()

    network.send("enrollment", f"{username};{password};;{client.get_voltage_lut()}")
    salt = network.receive("handshake")

    client.handshake(password, bytes(salt, "utf-8"))

    try:
        while True:
            cipher = network.receive(username)
            client.decrypt(cipher)
    except KeyboardInterrupt():
        exit(0)


if __name__ == '__main__':
    main()
