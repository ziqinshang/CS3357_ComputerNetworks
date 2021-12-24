import socket
import argparse
import sys
from sys import stdin
from urllib.parse import urlparse
import signal
import select

# Define a constant for our buffer size

BUFFER_SIZE = 2048


# Our main function

def main():
    # Register our signal handler for shutting down.
    def signal_handler(sig, frame):
        print('Interrupt received, shutting down ...')
        msg_tosend = "Disconnect" + user_name + "CHAT/1.0"
        msg_tosend = msg_tosend.encode()
        client_socket.send(msg_tosend)  # at least send some message before you die!
        client_socket.close()
        sys.exit(0)

    # Check command line arguments to retrieve a URL.
    # USAGE : chat://host:port
    signal.signal(signal.SIGINT, signal_handler)
    # retrive the user name, port and host specifications from command line parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="User name")
    parser.add_argument("url", help="URL to the server")
    args = parser.parse_args()
    user_name = args.username
    o = urlparse(args.url)
    host = o.hostname
    port = int(o.port)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('\nConnecting to the chat server')
    client_socket.connect((host, port))
    print('\nConnection Established')
    client_socket.send(user_name.encode())
    # Now we try to make a connection to the server.
    while 1:
        # same thing, this time the socket list is only stdin and yourself
        # cuz you only need talk to the server and the server will do all the hard work
        socket_list = [sys.stdin, client_socket]
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        # same logic as server.py
        for skt in read_sockets:
            # this is for receiving message
            if skt == client_socket:
                data = skt.recv(BUFFER_SIZE)
                if not data: # if there is no data coming, means the server has shut down
                    client_socket.close() # close the connection with server
                    print('\nDISCONNECT CHAT/1.0')
                    sys.exit(0)
                print(data.decode()) # if there is some data, print it!
            # and this is for the sending message
            else:
                msg = sys.stdin.readline() # read the input message from user via stdin
                msg_tosend = "@" + user_name + ":" + msg # construct the message with your username
                msg_tosend = msg_tosend.encode() # encode it
                client_socket.send(msg_tosend) # and send
                sys.stdout.flush()


#
# def signal_handler(sig, frame):
#     print('Interrupt received, shutting down ...')
#     sys.exit(0)

if __name__ == '__main__':
    main()
