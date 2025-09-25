#!/bin/python3

import socket
import sys

def main():
    if not len(sys.argv) == 2:
        print("Usage: chat_server.py <port #>")
    else:
        port = sys.argv[1]
        try:
            (int(port))
        except ValueError:
            print('Port should be an integer in the range 1024-49151')
    if not port in range(1024, 49151):
        print('Port should be an integer in the range 1024-49151')

    

if __name__ == '__main__':
    main()
