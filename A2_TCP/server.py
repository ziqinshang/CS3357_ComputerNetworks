import socket
import os
import datetime
import signal
import sys
import select

# Constant for our buffer size
BUFFER_SIZE = 2048
socket_list = []
client_list = []


# Our main function.
def main():
    # Register our signal handler for shutting down.
    def signal_handler(sig, frame):
        print('Interrupt received, shutting down ...')
        # close every single sockets in the registered socket list before shut down
        for sockets in socket_list:
            sockets.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    # Create the socket. The port number is set to be 50000 for the development/debugging process
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(0)  # non-blocking I/O
    server_socket.bind(('', 50000))
    server_socket.listen(10)  # listening to 10 clients at a time
    socket_list.append(server_socket)  # add this server socket into acceptable socket list
    # print the instruction message
    print('Will wait for client messages at port ' + str(server_socket.getsockname()[1]))

    # Keep the server running forever.
    while (1):
        # what select really do is to maintain a list of available I/Os, this confused me for a while
        # so basically ready_to_read is the socket list, but it will only become available for access
        # if it received any kind of signals, ready_to_write and in_error are not used because there is
        # no requirement for write(not really worth to be implemented) and error
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
        for skt in ready_to_read:  # for every available socket to read from
            if skt == server_socket:  # if the socket is server socket, means there is a new connection coming
                sockfd, addr = server_socket.accept()  # so we gladly accept it
                socket_list.append(sockfd)  # and add it to our socket list
                usrname = sockfd.recv(BUFFER_SIZE)  # get the user name input from client and show it
                print("Client %s connected" % usrname.decode())
            else:
                try:
                    # an attempt to remove a client once the socket is closed, nice try tho
                    # if(skt.fileno()==-1):
                    #     ready_to_read.remove(skt)
                    data = skt.recv(BUFFER_SIZE) # read the data from client socket
                    # this is what end up really worked for removing client if closed socket
                    if not data: # if there is nothing in that socket
                        socket_list.remove(skt) # remove it from registered socket list
                        break # and end the for loop
                    print(data.decode()) # if there is data, show it!
                    for client in socket_list: # a broadcast function
                        if client != server_socket: # if the socket we are broadcasting is not a server socket
                            if client != skt: # and if it is not itself
                                client.send(data) # then send what you gotta say
                except: # this dont really work so I will leave it here
                    print("Client (%s, %s) is offline\n" % addr)
                    continue


if __name__ == '__main__':
    main()
