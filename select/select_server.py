# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    server = socket.socket()
    server.bind(('localhost', port))
    server.listen()

    connections = {server}

    while(True):
        ready, _, _ = select.select(connections, {}, {})

        for connection in ready:
            if connection == server:
                conn, address = server.accept()
                connections.add(conn)
                print(address, ': connected')
            else:
                message = connection.recv(4096)
                if not message == b'':
                    print(connection.getpeername(), len(message), 'bytes:', message)
                else:
                    print(connection.getpeername(), ': disconnected')
                    connections.remove(connection)
                    connection.close()
                    


#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
