import argparse

from getpass import getpass
from reram_puf import __version__
from reram_puf.client.client import Client


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

    return parser.parse_args()


def main():
    args = parse_args()
    client = Client(port=args.serial_port, baudrate=args.baud_rate)
    password = getpass()
    try:
        pass
    except KeyboardInterrupt():
        exit(0)


if __name__ == '__main__':
    main()
