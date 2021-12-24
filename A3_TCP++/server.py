import socket
import os
import signal
import sys
import time
import selectors

# Selector for helping us select incoming data and connections from multiple sources.

sel = selectors.DefaultSelector()

# Client list for mapping connected clients to their connections.

client_list = []
follow_list = []
file_specs = []

# Signal handler for graceful exiting.  We let clients know in the process so they can disconnect too.

def signal_handler(sig, frame):
    print('Interrupt received, shutting down ...')
    message='DISCONNECT CHAT/1.0\n'
    for reg in client_list:
        reg[1].send(message.encode())
    sys.exit(0)

# Read a single line (ending with \n) from a socket and return it.
# We will strip out the \r and the \n in the process.

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

# Search the client list for a particular user.

def client_search(user):
    for reg in client_list:
        if reg[0] == user:
            return reg[1]
    return None

# Search the client list for a particular user by their socket.

def client_search_by_socket(sock):
    for reg in client_list:
        if reg[1] == sock:
            return reg[0]
    return None

# Add a user to the client list.

def client_add(user, conn):
    registration = (user, conn)
    client_list.append(registration)
    atuser = "@" + user
    tmplist = [user,atuser,"@all"]
    follow_list.append(tmplist)

# Remove a client when disconnected.

def client_remove(user):
    for reg in client_list:
        if reg[0] == user:
            client_list.remove(reg)
            break

# Function to read messages from clients.

def read_message(sock, mask):
    message = get_line_from_socket(sock)

    # Does this indicate a closed connection?

    if message == '':
        print('Closing connection')
        sel.unregister(sock)
        sock.close()

    # Receive the message.  

    else:
        user = client_search_by_socket(sock)
        print(f'Received message from user {user}:  ' + message)
        words = message.split(' ')

        # Check for client disconnections.
        if words[0] == 'DISCONNECT':
            print('Disconnecting user ' + user)
            client_remove(user)
            sel.unregister(sock)
            sock.close()

        # The !attach command is realized with 8 Steps between server and client.
        # STEP1: client send !attach [filename] to the server
        # STEP2: server received 1st message, send a message that request for filesize, format: FILEREAD2 filename
        # STEP3: client received 2nd message, send a message that contains filesize
        # STEP4: server received 3rd message, inform the client that the server is ready to receive file
        # STEP5: client send data through socket with pre-defined file size
        # STEP6: server received data, write the data into server folder
        # STEP7: server send message to clients that has this file followed to inform them there is a incoming file
        # STEP8: client open socket with filesize and write the data into newly created file

        # STEP1: client send !attach [filename] to the server
        if words[1] == '!attach':
            filename = words[2]
            readmsg = "FILEREAD2 " + filename
            readmsg = f'{readmsg}\n'
            # STEP2: server received 1st message, send a message that request for filesize, format: FILEREAD2 filename
            sock.send(readmsg.encode())

        if words[0] == 'FILESPECS':
            filename = words[1]
            filesize = words[2]
            filesize = int(filesize)
            filenameandtype = filename.split(".")
            filetype = filenameandtype[1]
            filetuple = (filename,filesize)
            file_specs.append(filetuple)
            readymsg = "SERVERREADY " + filename
            readymsg = f'{readymsg}\n'
            # STEP4: server received 3rd message, inform the client that the server is ready to receive file
            sock.send(readymsg.encode())
            time.sleep(1)
            #data = sock.recv(filesize).decode()
            # STEP6: server received data, write the data into server folder
            if (filetype == 'txt'):
                data = sock.recv(filesize).decode()
                with open(filename, "w") as f:
                        print('Incoming File :' + filename)
                        print("Content Length: " + str(filesize))
                        bytes_read = data
                        f.write(bytes_read)
                print("File "+filename+" written to server")
            elif (filetype == 'bin'):
                data = sock.recv(filesize)
                with open(filename, "wb") as f:
                        print('Incoming File :' + filename)
                        print("Content Length: " + str(filesize))
                        bytes_read = data
                        f.write(bytes_read)
                print("File "+filename+" written to server")
            else:
                data = sock.recv(filesize)
                with open(filename, "wb") as f:
                        print('Incoming File :' + filename)
                        print("Content Length: " + str(filesize))
                        bytes_read = data
                        f.write(bytes_read)
                print("File "+filename+" written to server")
            # STEP7: server send message to clients that has this file followed to inform them there is a incoming file
            writemsg = "FILEWRITE2 " + filename + " " + str(filesize)
            writemsg = f'{writemsg}\n'
            for follow in follow_list:
                for word in words:
                    if word in follow:
                        for reg in client_list:
                            if reg[0] == follow[0]:
                                client_sock = reg[1]
                                client_sock.send(writemsg.encode())

        if words[0] == 'CLIENTREADY':
            filename = words[1]
            filenameandtype = filename.split(".")
            filetype = filenameandtype[1]
            filesize = os.path.getsize(filename)
            if (filetype == 'txt'):
                with open(filename, "r") as f:
                    bytes_read = f.read(filesize)
                    sock.send(bytes_read.encode())
                f.close()
            elif (filetype == 'bin'):
                with open(filename, "rb") as f:
                    bytes_read = f.read(filesize)
                    sock.send(bytes_read)
                f.close()
            else:
                with open(filename, "rb") as f:
                    bytes_read = f.read(filesize)
                    sock.send(bytes_read)
                f.close()

        if words[1] == '!attach2':
            filename = words[2]
            readmsg = "FILEREAD " + filename
            tmpsocket = client_search(user)
            readmsg = f'{readmsg}\n'
            tmpsocket.send(readmsg.encode())
            time.sleep(1)
            filespecs = get_line_from_socket(sock)
            #time.sleep(1)
            filewords = filespecs.split(" ")
            print(filewords)
            filesize = filewords[1]
            filesize = int(filesize)
            filecontent = filewords[2]
            print(filecontent)
            writemsg = "FILEWRITE " + filename + " " + str(filesize) + " " + filecontent
            writemsg = f'{writemsg}\n'
            for follow in follow_list:
                for word in words:
                    if word in follow:
                        for reg in client_list:
                            if reg[0] == follow[0]:
                                client_sock = reg[1]
                                client_sock.send(writemsg.encode())

        if words[1] == '!list':
            listofclient = []
            for client in client_list:
                listofclient.append(client[0])
            whole = ",".join(listofclient)
            tmpsocket = client_search(user)
            forwarded_message = f'{whole}\n'
            tmpsocket.send(forwarded_message.encode())

        if words[1] == '!follow':
            if len(words) > 3:
                writemsg = "ERROR: Attempt to follow multiple term"
                writemsg = f'{writemsg}\n'
                sock.send(writemsg.encode())
            else:
                for follow in follow_list:
                    if follow[0] == user:
                        if words[2] in follow:
                            writemsg = "ERROR: Attempts to follow a term multiple times"
                            writemsg = f'{writemsg}\n'
                            sock.send(writemsg.encode())
                        else:
                            print('follow list for ' + user + " updated")
                            follow.append(words[2])
                            print(follow)
                            writemsg = "Now following " + words[2]
                            writemsg = f'{writemsg}\n'
                            sock.send(writemsg.encode())
                # for follow in follow_list:
                #     if follow[0] == user:
                #         print('follow list for ' + user + " updated")
                #         follow.append(words[2])
                #         print(follow)

        if words[1] == '!unfollow':
            for follow in follow_list:
                if follow[0] == user:
                    if words[2] not in follow:
                        writemsg = "ERROR: Attempts to remove a term not being followed"
                        writemsg = f'{writemsg}\n'
                        sock.send(writemsg.encode())
                    elif (words[2] == '@all' or words[2] == '@' + user):
                        writemsg = "ERROR: Attempts to remove a term that cannot be unfollowed"
                        writemsg = f'{writemsg}\n'
                        sock.send(writemsg.encode())
                    else:
                        print('follow list for ' + user + " updated")
                        follow.remove(words[2])
                        print(follow)

        if words[1] == "!follow?":
            print('printing follow list for' + user)
            tmpfollow = []
            for follow in follow_list:
                if follow[0] == user:
                    tmpfollow = follow
            whole = ",".join(tmpfollow)
            tmpsocket = client_search(user)
            forwarded_message = f'{whole}\n'
            tmpsocket.send(forwarded_message.encode())

        if words[1] == '!exit':
            print('Disconnecting user ' + user)
            forwarded_message = f'{"DISCONNECT"}\n'
            sock.send(forwarded_message.encode())
            client_remove(user)
            sel.unregister(sock)
            sock.close()

        # Send message to all users.  Send at most only once, and don't send to yourself. 
        # Need to re-add stripped newlines here.

        else:
            for follow in follow_list:
                for word in words:
                    if word in follow:
                        for reg in client_list:
                            if reg[0] == follow[0]:
                                client_sock = reg[1]
                                forwarded_message = f'{message}\n'
                                client_sock.send(forwarded_message.encode())
# Function to accept and set up clients.

def accept_client(sock, mask):
    conn, addr = sock.accept()
    print('Accepted connection from client address:', addr)
    message = get_line_from_socket(conn)
    message_parts = message.split()

    # Check format of request.

    if ((len(message_parts) != 3) or (message_parts[0] != 'REGISTER') or (message_parts[2] != 'CHAT/1.0')):
        print('Error:  Invalid registration message.')
        print('Received: ' + message)
        print('Connection closing ...')
        response='400 Invalid registration\n'
        conn.send(response.encode())
        conn.close()

    # If request is properly formatted and user not already listed, go ahead with registration.

    else:
        user = message_parts[1]

        if ((client_search(user) == None) and (user != "all")):
            client_add(user,conn)
            print(f'Connection to client established, waiting to receive messages from user \'{user}\'...')
            response='200 Registration succesful\n'
            conn.send(response.encode())
            conn.setblocking(False)
            #conn.setblocking(True)
            sel.register(conn, selectors.EVENT_READ, read_message)

        # If user already in list, return a registration error.

        else:
            print('Error:  Client already registered.')
            print('Connection closing ...')
            response='401 Client already registered\n'
            conn.send(response.encode())
            conn.close()


# Our main function.

def main():

    # Register our signal handler for shutting down.

    signal.signal(signal.SIGINT, signal_handler)

    # Create the socket.  We will ask this to work on any interface and to pick
    # a free port at random.  We'll print this out for clients to use.

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 0))
    print('Will wait for client connections at port ' + str(server_socket.getsockname()[1]))
    server_socket.listen(100)
    server_socket.setblocking(False)
    sel.register(server_socket, selectors.EVENT_READ, accept_client)
    print('Waiting for incoming client connections ...')
     
    # Keep the server running forever, waiting for connections or messages.
    
    while(True):
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)    

if __name__ == '__main__':
    main()

