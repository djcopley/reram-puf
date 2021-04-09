import argparse

from getpass import getpass

from reram_puf.common.network import Network
from reram_puf import __version__
from reram_puf.client.client import Client


# Define callback function for MQTT message callback
def on_message(client, userdata, message):
    """Callback function for receiving messages."""
    msg = message.payload
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
    parser.add_argument("--serial_port",
                        type=str,
                        help="the serial port of arduino puf",
                        default="COM4")

    parser.add_argument("--baud_rate",
                        type=str,
                        help="the arduino serial baud rate",
                        default="115200")

    parser.add_argument("--host", type=str,
                        help="Hostname to connect to for network communication.",
                        default="192.168.0.2")

    parser.add_argument("--client", type=str,
                        help="Name of the client who is connecting to the network.",
                        default="client")

    return parser.parse_args()


def main():
    args = parse_args()
    client = Client(port=args.serial_port, baudrate=args.baud_rate)

    global network
    network = Network(args.host, args.client)
    network.mqtt.client.on_message = on_message
    network.connect()

    username = input("Please enter username: ")
    password = getpass()

    network.send("enrollment", f"{username};{password};;{client.get_voltage_lut()}")
    salt = network.receive("handshake")

    client.handshake(password, salt)

    try:
        while True:
            cipher = network.receive(username)
            print(type(cipher))
            plaintext = client.decrypt(cipher)
            print(f"PLAINTEXT: {plaintext}")
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
