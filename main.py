import fazip
import sys


def do_extraction():
    pass


def do_compression():
    pass


def print_help():
    pass


if __name__ == '__main__':
    print(sys.argv)
    if sys.argv[1] == 'x' and len(sys.argv) == 3:
        do_extraction()
    elif sys.argv[1] == 'c' and len(sys.argv) >= 4:
        do_compression()
    else:
        print_help()
