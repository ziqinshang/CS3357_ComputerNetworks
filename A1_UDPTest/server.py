import socket
import os
import datetime
import signal
import sys

# Constant for our buffer size

BUFFER_SIZE = 2048

# Signal handler for graceful exiting.

def signal_handler(sig, frame):
    print('Interrupt received, shutting down ...')
    sys.exit(0)

# Our main function.

def main():

    # Register our signal handler for shutting down.

    signal.signal(signal.SIGINT, signal_handler)

    # Create the socket.  We will ask this to work on any interface and to pick
    # a free port at random.  We'll print this out for clients to use.

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 0))
    print('Will wait for client messages at port ' + str(server_socket.getsockname()[1]))
    
    # Keep the server running forever.
    
    while(1):
        print('Waiting for incoming client message ...')
        message, addr = server_socket.recvfrom(BUFFER_SIZE)
        print('Message received from client address:', addr)
        print('Message:')
        print(message.decode())

if __name__ == '__main__':
    main()

