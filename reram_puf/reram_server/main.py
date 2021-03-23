import argparse

from reram_puf import __version__


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__
    )
    return parser.parse_args()


def main():
    pass


if __name__ == '__main__':
    main()
