import socket
import os
import signal
import sys
import argparse
from urllib.parse import urlparse
import time
import selectors

BUFFER_SIZE = 1024
# Selector for helping us select incoming data from the server and messages typed in by the user.

sel = selectors.DefaultSelector()

# Socket for sending messages.

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# User name for tagging sent messages.

user = ''


# Signal handler for graceful exiting.  Let the server know when we're gone.

def signal_handler(sig, frame):
    print('Interrupt received, shutting down ...')
    message = f'DISCONNECT {user} CHAT/1.0\n'
    client_socket.send(message.encode())
    sys.exit(0)


# Simple function for setting up a prompt for the user.

def do_prompt(skip_line=False):
    if (skip_line):
        print("")
    print("> ", end='', flush=True)


# Read a single line (ending with \n) from a socket and return it.
# We will strip out any \r and \n in the process.

def get_line_from_socket(sock):
    done = False
    line = ''
    while (not done):
        char = sock.recv(1).decode()
        if (char == '\r'):
            pass
        elif (char == '\n'):
            done = True
        else:
            line = line + char
    return line


# Function to handle incoming messages from server.  Also look for disconnect messages to shutdown.

# Usage:
# !attach [filename] :
# send the file [filename] in current folder to every user who has [filename] registered in their following list
# !attach2 [filename] :
# an early attempt of !attach, did not work out too well but I choose to keep it anyways
# !follow [keyword]:
# follow a certain keyword, only messages contain followed keywords will be displayed in client side
# !unfollow [keyword]:
# unfollow a certain keyword, messages contain unfollowed keywords will not be displayed in client side
# !follow? :
# list current following keywords
# !exit :
# disconnect from server and close the program
# !list :
# list the current clients connected to the server

def handle_message_from_server(sock, mask):
    message = get_line_from_socket(sock)
    words = message.split(' ')
    if words[0] == 'DISCONNECT':
        print('Disconnected from server ... exiting!')
        sys.exit(0)

    # The !attach command is realized with 8 Steps between server and client.
    # STEP1: client send !attach [filename] to the server
    # STEP2: server received 1st message, send a message that request for filesize, format: FILEREAD2 filename
    # STEP3: client received 2nd message, send a message that contains filesize
    # STEP4: server received 3rd message, inform the client that the server is ready to receive file
    # STEP5: client send data through socket with pre-defined file size
    # STEP6: server received data, write the data into server folder
    # STEP7: server send message to clients that has this file followed to inform them there is a incoming file
    # STEP8: client open socket with filesize and write the data into newly created file

    # STEP3: client received 2nd message, send a message that contains filesize
    elif words[0] == 'FILEREAD2':
        filename = words[1]
        if(os.path.isfile(filename)):
            filesize = os.path.getsize(filename)
            filecontent = ""
            filenameandtype = filename.split(".")
            filetype = filenameandtype[1]
            filespecs = "FILESPECS " + filename + " " + str(filesize)
            filespecs = f'{filespecs}\n'
            sock.send(filespecs.encode())
        else:
            errormsg = "FILE " + filename + " does not exist"
            print(errormsg)
            errormsg = f'{errormsg}\n'
            sock.send(errormsg.encode())

    elif words[0] == 'SERVERREADY':
        filename = words[1]
        filenameandtype = filename.split(".")
        filetype = filenameandtype[1]
        filesize = os.path.getsize(filename)
        # STEP5: client send data through socket with pre-defined file size
        if (filetype == 'txt'):
            with open(filename, "r") as f:
                bytes_read = f.read(filesize)
                sock.send(bytes_read.encode())
            f.close()
            print("File " + filename + " sent to server")
        elif (filetype == 'bin'):
            with open(filename, "rb") as f:
                bytes_read = f.read(filesize)
                sock.send(bytes_read)
            f.close()
            print("File " + filename + " sent to server")

    # STEP8: client open socket with filesize and write the data into newly created file
    elif words[0] == 'FILEWRITE2':
        filename = words[1]
        filenameandtype = filename.split(".")
        filetype = filenameandtype[1]
        filesize = words[2]
        filesize = int(filesize)
        readymsg = "CLIENTREADY " + filename + " " +str(filesize)
        readymsg = f'{readymsg}\n'
        sock.send(readymsg.encode())
        time.sleep(1)
        #data = sock.recv(filesize).decode()
        if (filetype == 'txt'):
            data = sock.recv(filesize).decode()
            with open(filename, "w") as f:
                print('Incoming File :' + filename)
                print("Content Length: " + str(filesize))
                bytes_read = data
                f.write(bytes_read)
            print("File " + filename + " written to client")
        elif (filetype == 'bin'):
            data = sock.recv(filesize)
            with open(filename, "wb") as f:
                print('Incoming File :' + filename)
                print("Content Length: " + str(filesize))
                bytes_read = data
                f.write(bytes_read)
            print("File " + filename + " written to client")


    elif words[0] == 'FILEREAD':
        filename = words[1]
        filesize = os.path.getsize(filename)
        filecontent = ""
        filenameandtype = filename.split(".")
        filetype = filenameandtype[1]
        if(filetype == 'txt'):
            with open(filename, "r") as f:
                bytes_read = f.read(filesize)
                filecontent = bytes_read
                filespecs = filename + " " + str(filesize) + " " + filecontent
                print(filespecs)
                filespecs = f'{filespecs}\n'
                sock.send(filespecs.encode())
            f.close()
        elif(filetype == 'bin'):
            with open(filename, "rb") as f:
                bytes_read = f.read(filesize)
                filecontent = bytes_read
                filecontent = filecontent.decode('ASCII')
                filespecs = filename + " " + str(filesize) + " " + filecontent
                print(filespecs)
                filespecs = f'{filespecs}\n'
                sock.send(filespecs.encode())
            f.close()
        else:
            with open(filename, "rb") as f:
                bytes_read = f.read(filesize)
                filecontent = bytes_read
                filecontent = filecontent.decode('ASCII')
                filespecs = filename + " " + str(filesize) + " " + filecontent
                print(filespecs)
                filespecs = f'{filespecs}\n'
                sock.send(filespecs.encode())
            f.close()

    elif words[0] == 'FILEWRITE':
        filename = words[1]
        filenameandtype = filename.split(".")
        filetype = filenameandtype[1]
        filesize = words[2]
        filesize = int(filesize)
        filecontent = ""
        for word in words:
            if word == filename: continue
            if word == filesize: continue
            filecontent = filecontent + " " + word
        #filecontent = words[3]
        if (filetype == "txt"):
            with open(filename, "w") as f:
                print('Incoming File :' + filename)
                print("Content Length: " + str(filesize))
                bytes_read = filecontent
                f.write(bytes_read)
        elif(filetype == "bin"):
            with open(filename, "wb") as f:
                print('Incoming File :' + filename)
                print("Content Length: " + str(filesize))
                bytes_read = filecontent.encode('ASCII')
                f.write(bytes_read)
        else:
            with open(filename, "wb") as f:
                print('Incoming File :' + filename)
                print("Content Length: " + str(filesize))
                bytes_read = filecontent.encode('ASCII')
                f.write(bytes_read)
            # print('File' + filename +"received from server and written ... exiting!")
            # sys.exit(0)
    else:
        print(message)
        do_prompt()


# Function to handle incoming messages from user.

def handle_keyboard_input(file, mask):
    line = sys.stdin.readline()
    message = f'@{user}: {line}'
    client_socket.send(message.encode())
    do_prompt()


# Our main function.

def main():
    global user
    global client_socket

    # Register our signal handler for shutting down.

    signal.signal(signal.SIGINT, signal_handler)

    # Check command line arguments to retrieve a URL.

    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="user name for this user on the chat service")
    parser.add_argument("server", help="URL indicating server location in form of chat://host:port")
    args = parser.parse_args()

    # Check the URL passed in and make sure it's valid.  If so, keep track of
    # things for later.

    try:
        server_address = urlparse(args.server)
        if ((server_address.scheme != 'chat') or (server_address.port == None) or (server_address.hostname == None)):
            raise ValueError
        host = server_address.hostname
        port = server_address.port
    except ValueError:
        print('Error:  Invalid server.  Enter a URL of the form:  chat://host:port')
        sys.exit(1)
    user = args.user

    # Now we try to make a connection to the server.

    print('Connecting to server ...')
    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print('Error:  That host or port is not accepting connections.')
        sys.exit(1)

    # The connection was successful, so we can prep and send a registration message.

    print('Connection to server established. Sending intro message...\n')
    message = f'REGISTER {user} CHAT/1.0\n'
    client_socket.send(message.encode())

    # Receive the response from the server and start taking a look at it

    response_line = get_line_from_socket(client_socket)
    response_list = response_line.split(' ')

    # If an error is returned from the server, we dump everything sent and
    # exit right away.  

    if response_list[0] != '200':
        print('Error:  An error response was received from the server.  Details:\n')
        print(response_line)
        print('Exiting now ...')
        sys.exit(1)
    else:
        print('Registration successful.  Ready for messaging!')

    # Set up our selector.

    client_socket.setblocking(False)
    sel.register(client_socket, selectors.EVENT_READ, handle_message_from_server)
    sel.register(sys.stdin, selectors.EVENT_READ, handle_keyboard_input)

    # Prompt the user before beginning.

    do_prompt()

    # Now do the selection.

    while (True):
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    main()
