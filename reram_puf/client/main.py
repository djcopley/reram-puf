import argparse

from reram_puf import __version__
from client import Client


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
    return parser.parse_args()


def main():
    args = parse_args()
    client = Client(port=args.port)
    try:
        client.run()
    except KeyboardInterrupt():
        exit(0)


if __name__ == '__main__':
    main()
