import argparse

from ...reram_puf import __version__
from ..common.network import Network


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", 
        version=__version__)
    parser.add_argument("-h", "--hostname", type=str, required=True,
        help="Hostname to connect to for network communication.")
    parser.add_argument("-c", "--client", type=str, required=True,
        help="Name of the client who is connecting to the network.")
    return parser.parse_args()


def main():
    args = parse_args()
    network = Network(args.hostname, args.client)
    msg = "Hello from Python"
    network.send(args.client, msg)


if __name__ == '__main__':
    main()
