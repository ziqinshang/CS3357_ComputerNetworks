import socket
import argparse
from sys import stdin

# Define a constant for our buffer size

BUFFER_SIZE = 2048

# Our main function.

def main():

    # Check command line arguments to retrieve a URL.

    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Host name of server")
    parser.add_argument("port", help="Port number of server")
    args = parser.parse_args()
    host = args.host
    port = int(args.port)

    # Now we try to make a connection to the server.

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for line in stdin:
        client_socket.sendto(line.rstrip().encode(), (host,port))
    client_socket.close()


if __name__ == '__main__':
    main()
