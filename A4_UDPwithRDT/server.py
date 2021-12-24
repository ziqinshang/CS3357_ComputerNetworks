import socket
import os
import datetime
import signal
import sys
import select
import selectors
import struct
import hashlib
from string import punctuation

# Hard code location of the server.  Not what we'll want to be doing in the assignment,
# but okay for an example like this.

UDP_IP = "localhost"
UDP_PORT = 54321
TIMEOUT = 0.5  # retransmission timeout duration
# Constant for our buffer size
BUFFER_SIZE = 1024
CHUNKPACK_SIZE = 1064 # 4 + 4 + 32 + 1024
MAX_STRING_SIZE = 256
TYPE_ACK = 11  # 11 means ACK
sequence_num = 0
sequence_num_file = 0
peer_addr = ()
# Selector for helping us select incoming data and connections from multiple sources.

sel = selectors.DefaultSelector()

# Client list for mapping connected clients to their connections.

client_list = []
client_list_udp = []
client_list_udp2 = []


# Signal handler for graceful exiting.  We let clients know in the process so they can disconnect too.

def signal_handler(sig, frame):
    print('Interrupt received, shutting down ...')
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

def client_search_udp(user):
    for reg in client_list_udp:
        if reg[0] == user:
            return reg[1]
    return None

def client_search_udp2(user):
    for reg in client_list_udp2:
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

def client_add_udp(user, follow_terms):
    registration = (user, follow_terms)
    client_list_udp.append(registration)

def client_add_udp2(user, addr, follow_terms):
    registration = (user, addr, follow_terms)
    client_list_udp2.append(registration)

# Remove a client when disconnected.

def client_remove_udp(user):
    for reg in client_list_udp2:
        if reg[0] == user:
            client_list.remove(reg)
            break

# Function to list clients.

def list_clients_udp():
    first = True
    list = ''
    for reg in client_list_udp2:
        if first:
            list = reg[0]
            first = False
        else:
            list = f'{list}, {reg[0]}'
    return list

# Function to return list of followed topics of a user.

def client_follows_udp(user):
    for reg in client_list_udp:
        if reg[0] == user:
            first = True
            list = ''
            for topic in reg[1]:
                if first:
                    list = topic
                    first = False
                else:
                    list = f'{list}, {topic}'
            return list
    return None

def client_follows_udp2(user):
    for reg in client_list_udp2:
        if reg[0] == user:
            first = True
            list = ''
            for topic in reg[2]:
                if first:
                    list = topic
                    first = False
                else:
                    list = f'{list}, {topic}'
            return list
    return None
# Function to add to list of followed topics of a user, returning True if added or False if topic already there.

def client_add_follow_udp(user, topic):
    for reg in client_list_udp:
        if reg[0] == user:
            if topic in reg[1]:
                return False
            else:
                reg[1].append(topic)
                return True
    return None
def client_add_follow_udp2(user, topic):
    for reg in client_list_udp2:
        if reg[0] == user:
            if topic in reg[2]:
                return False
            else:
                reg[2].append(topic)
                return True
    return None

# Function to remove from list of followed topics of a user, returning True if removed or False if topic was not already there.

def client_remove_follow_udp(user, topic):
    for reg in client_list_udp:
        if reg[0] == user:
            if topic in reg[1]:
                reg[1].remove(topic)
                return True
            else:
                return False
    return None

def client_remove_follow_udp2(user, topic):
    for reg in client_list_udp2:
        if reg[0] == user:
            if topic in reg[2]:
                reg[2].remove(topic)
                return True
            else:
                return False
    return None


# Function to accept and set up clients.
def accept_client(sock, mask):
    global sequence_num_file
    global sequence_num
    message ,addr = rdt_recv(sock)
    message_parts = message.split()

    # Check format of request.
    if (message_parts[1] == '!attachment'):
        user = message_parts[0]
        filename = message_parts[2]
        response = f'ATTACH2 {filename} CHAT/1.0\n'
        rdt_send(sock, addr, response)
        msg, addr = rdt_recv(sock)
        msg_parts = msg.split()
        if (len(msg_parts) != 2) or (msg_parts[0] != 'Content-Length:'):
            response = f'Error:  Invalid attachment header\n'
            rdt_send(sock,addr, response)
        elif msg_parts[1] == '-1':
            response = f'Error:  Attached file {filename} could not be sent\n'
            rdt_send(sock, addr,response)
        else:
            bytes_read = 0
            bytes_to_read = int(msg_parts[1])
            with open(filename, 'wb') as file_to_write:
                while (bytes_read < bytes_to_read):
                    chunk = rdt_recv_file(sock)
                    print(bytes_read)
                    bytes_read += len(chunk)
                    sequence_num_file += 1
                    file_to_write.write(chunk)
            sequence_num_file = 0
            interested_clients = []
            attach_size = msg_parts[1]
            attach_notice = f'ATTACHMENT {filename} CHAT/1.0 Origin: {user} Content-Length: {attach_size}'
            for reg in client_list_udp2:
                if reg[0] == user:
                    continue
                forwarded = False
                for term in reg[2]:
                    for word in message_parts:
                        if ((term == word.rstrip(punctuation)) and not forwarded):
                            interested_clients.append(reg[1])
                            rdt_send(sock,reg[1],attach_notice)
                            forwarded = True
            with open(filename, 'rb') as file_to_send:
                while True:
                    chunk = file_to_send.read(BUFFER_SIZE)
                    if chunk:
                        for client in interested_clients:
                            rdt_send_file(sock, client ,chunk)
                        sequence_num_file += 1
                    else:
                        break
            sequence_num_file = 0
        response2 = f'Attachment {filename} attached and distributed\n'
        rdt_send(sock, addr, response2)


    if (client_search_udp2(message_parts[0]) != None):

        user = message_parts[0]
        if ((len(message_parts) == 2) and ((message_parts[1] == '!list') or (message_parts[1] == '!exit') or (message_parts[1] == '!follow?'))):
            if message_parts[1] == '!list':
                response = list_clients_udp() + '\n'
                rdt_send(sock, addr,response)
            elif message_parts[1] == '!exit':
                print('Disconnecting user ' + user)
                response = 'DISCONNECT CHAT/1.0\n'
                rdt_send(sock, addr,response)
                client_remove_udp(user)
            elif message_parts[1] == '!follow?':
                response = client_follows_udp2(user) + '\n'
                rdt_send(sock,addr, response)

        elif ((len(message_parts) == 3) and ((message_parts[1] == '!follow') or (message_parts[1] == '!unfollow'))):
            if message_parts[1] == '!follow':
                topic = message_parts[2]
                if client_add_follow_udp2(user, topic):
                    response = f'Now following {topic}\n'
                else:
                    response = f'Error:  Was already following {topic}\n'
                rdt_send(sock, addr,response)
            elif message_parts[1] == '!unfollow':
                topic = message_parts[2]
                if topic == '@all':
                    response = 'Error:  All users must follow @all\n'
                elif topic == user:
                    response = 'Error:  Cannot unfollow yourself\n'
                elif client_remove_follow_udp2(user, topic):
                    response = f'No longer following {topic}\n'
                else:
                    response = f'Error:  Was not following {topic}\n'
                rdt_send(sock, addr, response)
        else:
            for reg in client_list_udp2:
                if reg[0] == user:
                    continue
                forwarded = False
                for term in reg[2]:
                    for word in message_parts:
                        if ((term == word.rstrip(punctuation)) and not forwarded):
                            client_address = reg[1]
                            forwarded_message = f'{message}\n'
                            rdt_send(sock, client_address, forwarded_message)
                            forwarded = True


    elif ((len(message_parts) != 3) or (message_parts[1] != 'REGISTER') or (message_parts[2] != 'CHAT/1.0')):
        print('Error:  Invalid registration message.')
        print('Received: ' + message)
        print('Connection closing ...')
        response = '400 Invalid registration\n'
        rdt_send(sock,addr,response)

    # If request is properly formatted and user not already listed, go ahead with registration.

    else:
        user = message_parts[0]
        if user == '@all':
            print('Error:  Client cannot use reserved user name \'all\'.')
            print('Connection closing ...')
            response = '402 Forbidden user name\n'
            rdt_send(sock,addr,response)

        elif (client_search_udp2(user) == None):

            # # Check for following terms or an issue with the request.
            follow_terms = []
            follow_terms.append(f'{user}')
            follow_terms.append('@all')

            # Finally add the user.

            client_add_udp2(user, addr, follow_terms)
            print(f'Connection to client established, waiting to receive messages from user \'{user}\'...')
            response = '200 Registration succesful\n'
            # conn.send(response.encode())
            # conn.setblocking(False)
            # sel.register(conn, selectors.EVENT_READ, read_message)
            rdt_send(sock,addr,response)

        # If user already in list, return a registration error.

        else:
            print('Error:  Client already registered.')
            print('Connection closing ...')
            response = '401 Client already registered\n'
            rdt_send(sock,addr, response)


def is_ack(recv_pkt, seq_num):
    global TYPE_ACK
    # Dissect the received packet
    unpacker = struct.Struct(f'I i 32s')
    ACK_UDP_packet = unpacker.unpack(recv_pkt)
    received_ACK = ACK_UDP_packet[0]
    received_sequence = ACK_UDP_packet[1]
    received_checksum = ACK_UDP_packet[2]
    values = (received_ACK, received_sequence)
    packer = struct.Struct(f'I i')
    packed_data = packer.pack(*values)
    computed_checksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    return received_ACK == TYPE_ACK and received_sequence == seq_num and received_checksum == computed_checksum


def make_ack(seq_num):
    # Make initial message
    global TYPE_ACK
    pre_packet_tuple = (TYPE_ACK, seq_num)
    msg_format = struct.Struct(f'I i')
    init_msg = msg_format.pack(*pre_packet_tuple)
    # Calculate checksum
    checksum = bytes(hashlib.md5(init_msg).hexdigest(), encoding="UTF-8")
    packet_tuple = (TYPE_ACK, seq_num, checksum)
    ACK_UDP_packet_structure = struct.Struct(f'I i 32s')
    ACK_UDP_packet = ACK_UDP_packet_structure.pack(*packet_tuple)
    # A complete msg with checksum
    return ACK_UDP_packet


def pack_data(data1, seq_num):
    # Our packet is going to contain a sequence number, our data, the size of our data, and a checksum.
    # Note that your packets may need to contain different things.
    data = data1.encode()
    size = len(data)
    # We now compute our checksum by building up the packet and running our checksum function on it.
    # Our packet structure will contain our sequence number first, followed by the size of the data,
    # followed by the data itself.  We fix the size of the string being sent ... as we are sending
    # less data, it will be padded with NULL bytes, but we can handle that on the receiving end
    # just fine!
    packet_tuple = (seq_num, size, data)
    packet_structure = struct.Struct(f'I I {MAX_STRING_SIZE}s')
    packed_data = packet_structure.pack(*packet_tuple)
    checksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    # Now we can construct our actual packet.  We follow the same approach as above, but now include
    # the computed checksum in the packet.
    packet_tuple = (seq_num, size, data, checksum)
    UDP_packet_structure = struct.Struct(f'I I {MAX_STRING_SIZE}s 32s')
    UDP_packet = UDP_packet_structure.pack(*packet_tuple)
    return UDP_packet

def pack_data_file(data1, seq_num):
    data = data1
    size = len(data)
    packet_tuple = (seq_num, size)
    packet_structure = struct.Struct(f'I I')
    packed_data = packet_structure.pack(*packet_tuple) + data
    checksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    packet_tuple = (seq_num, size, checksum)
    UDP_packet_structure = struct.Struct(f'I I 32s')
    UDP_packet = UDP_packet_structure.pack(*packet_tuple) + data
    return UDP_packet

def is_corrupt(udp_pkt):
    # Dissect received packet
    # We now compute the checksum on what was received to compare with the checksum
    # that arrived with the data.  So, we repack our received packet parts into a tuple
    # and compute a checksum against that, just like we did on the sending side.
    (received_sequence, received_size, received_data, received_checksum) = unpack_data(udp_pkt)
    values = (received_sequence, received_size, received_data)
    packer = struct.Struct(f'I I {MAX_STRING_SIZE}s')
    packed_data = packer.pack(*values)
    computed_checksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    # We can now compare the computed and received checksums to see if any corruption of
    # data can be detected.  Note that we only need to decode the data according to the
    # size we intended to send; the padding can be ignored.
    result = received_checksum != computed_checksum
    return result


def is_corrupt_file(udp_pkt):
    (received_sequence, received_size, received_checksum),data = unpack_data_file(udp_pkt)
    values = (received_sequence, received_size)
    packer = struct.Struct(f'I I')
    packed_data = packer.pack(*values) + data
    computed_checksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    result = received_checksum != computed_checksum
    return result

def unpack_data(received_packet):
    unpacker = struct.Struct(f'I I {MAX_STRING_SIZE}s 32s')
    UDP_packet = unpacker.unpack(received_packet)
    return UDP_packet

def unpack_data_file(received_packet):
    size = struct.calcsize(f'I I 32s')
    (seq_num, payload_len, recv_checksum), payload = struct.unpack(f'I I 32s', received_packet[:size]), received_packet[size:]
    return (seq_num, payload_len, recv_checksum), payload

def rdt_send(sock, address, data1):
    # Our packet is going to contain a sequence number, our data, the size of our data, and a checksum.
    # Note that your packets may need to contain different things.
    global sequence_num
    UDP_packet = pack_data(data1, sequence_num)
    # Finally, we can send out our packet over UDP and hope for the best.
    sock.sendto(UDP_packet, address)
    r_sock_list = [sock]  # Used in select.select()
    recv_expected = False  # Received expected response or not
    while not recv_expected:  # While not received expected ACK
        # Wait for ACK or timeout
        r, _, _ = select.select(r_sock_list, [], [], TIMEOUT)
        if r:  # ACK (or DATA) came
            for sock in r:
                # Try to receive ACK (or DATA)
                try:
                    recv_msg, addr = sock.recvfrom(1024)
                except socket.error as err_msg:
                    print("__udt_recv error: ", err_msg)
                    return -1
                # If corrupted or undesired ACK, keep waiting
                if is_ack(recv_msg, 1 - sequence_num):
                    print("rdt_send(): recv [corrupt] OR unexpected [ACK %d] | Keep waiting for ACK [%d]"
                          % (1 - sequence_num, sequence_num))
                # Happily received expected ACK
                elif is_ack(recv_msg, sequence_num):
                    print("rdt_send(): Received expected ACK [%d]!" % sequence_num)
                    return 0
        else:  # Timeout
            print("! TIMEOUT !")
            # Re-transmit packet
            try:
                sock.sendto(UDP_packet, address)
            except socket.error as err_msg:
                print("Socket send error: ", err_msg)
                return -1
            print("rdt_send(): Re-sent one message [%d] -> " % (sequence_num))


# Function to receive data in UDP
def rdt_recv(sock):
    global sequence_num
    global peer_addr
    recv_expected_data = False
    while not recv_expected_data:  # Repeat until received expected DATA
        try:
            received_packet, addr = sock.recvfrom(1024)
            peer_addr = addr
        except socket.error as err_msg:
            print("rdt_recv(): Socket receive error: " + str(err_msg))
            return b''
        UDP_packet = unpack_data(received_packet)
        received_sequence = UDP_packet[0]
        received_size = UDP_packet[1]
        received_data = UDP_packet[2]
        if is_corrupt(received_packet):
            print("rdt_recv(): Received [corrupted] packet")
            not_ack = make_ack(1 - sequence_num)
            try:
                sock.sendto(not_ack, addr)
            except socket.error as err_msg:
                print("rdt_recv(): Error in ACK-ing corrupt/wrong data packet: " + str(err_msg))
                return -1
        elif received_sequence != sequence_num:
            print("rdt_recv(): Received [wrong seq_num (%d)] Keep waiting for ACK [%d]" % (received_sequence,sequence_num))
            not_ack = make_ack(1 - sequence_num)
            try:
                sock.sendto(not_ack, addr)
            except socket.error as err_msg:
                print("rdt_recv(): Error in ACK-ing corrupt/wrong data packet: " + str(err_msg))
                return -1
        elif received_sequence == sequence_num:
            print("rdt_recv(): Received expected DATA [%d]" % (received_sequence))
            # print("Packet received from:", addr)
            # print('Received and computed checksums match, so packet can be processed')
            received_text = received_data[:received_size].decode()
            print(f'{received_text}')
            ack_msg = make_ack(sequence_num)
            try:
                #sock.sendto(ack_msg, (UDP_IP, UDP_PORT))
                sock.sendto(ack_msg, addr)
            except socket.error as err_msg:
                print("rdt_recv(): Error in ACK-ing expected data: " + str(err_msg))
                return b''
            print("rdt_recv(): Sent expected ACK [%d]" % received_sequence)
            #received_sequence ^= 1  # Flip seq num
            return received_text, addr

# Function to receive data in UDP
def rdt_recv_file(sock):
    global sequence_num_file
    global peer_addr
    recv_expected_data = False
    while not recv_expected_data:  # Repeat until received expected DATA
        try:
            received_packet, addr = sock.recvfrom(CHUNKPACK_SIZE)
            peer_addr = addr
        except socket.error as err_msg:
            print("rdt_recv_file(): Socket receive error: " + str(err_msg))
            return b''
        UDP_packet,data = unpack_data_file(received_packet)
        received_sequence = UDP_packet[0]
        received_size = UDP_packet[1]
        received_checksum = UDP_packet[2]
        if is_corrupt_file(received_packet):
            print("rdt_recv_file(): Received [corrupted] packet")
            not_ack = make_ack(1 - sequence_num_file)
            try:
                sock.sendto(not_ack, addr)
            except socket.error as err_msg:
                print("rdt_recv_file(): Error in ACK-ing corrupt/wrong data packet: " + str(err_msg))
                return -1
        elif received_sequence != sequence_num_file:
            print("rdt_recv_file(): Received [wrong seq_num (%d)] Keep waiting for ACK [%d]" % (received_sequence,sequence_num_file))
            not_ack = make_ack(1 - sequence_num_file)
            try:
                sock.sendto(not_ack, addr)
            except socket.error as err_msg:
                print("rdt_recv_file(): Error in ACK-ing corrupt/wrong data packet: " + str(err_msg))
                return -1
        elif received_sequence == sequence_num_file:
            print("rdt_recv_file(): Received expected DATA [%d]" % (received_sequence))
            # print("Packet received from:", addr)
            # print('Received and computed checksums match, so packet can be processed')
            received_chunk = data
            #print(f'Message text was:  {received_text}')
            ack_msg = make_ack(sequence_num_file)
            try:
                sock.sendto(ack_msg, addr)
            except socket.error as err_msg:
                print("rdt_recv_file(): Error in ACK-ing expected data: " + str(err_msg))
                return b''
            print("rdt_recv_file(): Sent expected ACK [%d]" % received_sequence)
            return received_chunk

def rdt_send_file(sock, address, data1):
    # Our packet is going to contain a sequence number, our data, the size of our data, and a checksum.
    # Note that your packets may need to contain different things.
    global sequence_num_file
    global host
    global port
    UDP_packet = pack_data_file(data1, sequence_num_file)
    # Finally, we can send out our packet over UDP and hope for the best.
    #sock.sendto(UDP_packet, (UDP_IP, UDP_PORT))
    sock.sendto(UDP_packet, address)
    r_sock_list = [sock]  # Used in select.select()
    recv_expected = False  # Received expected response or not
    while not recv_expected:  # While not received expected ACK
        # Wait for ACK or timeout
        r, _, _ = select.select(r_sock_list, [], [], TIMEOUT)
        if r:  # ACK (or DATA) came
            for sock in r:
                # Try to receive ACK (or DATA)
                try:
                    recv_msg, addr = sock.recvfrom(1024)
                except socket.error as err_msg:
                    print("__udt_recv error: ", err_msg)
                    return -1
                # If corrupted or undesired ACK, keep waiting
                if is_ack(recv_msg, 1 - sequence_num_file):
                    print("rdt_send_file(): recv [corrupt] OR unexpected [ACK %d] | Keep waiting for ACK [%d]"
                          % (1 - sequence_num_file, sequence_num_file))
                # Happily received expected ACK
                elif is_ack(recv_msg, sequence_num_file):
                    print("rdt_send_file(): Received expected ACK [%d]!" % sequence_num_file)
                    # sequence_num ^= 1  # Flip sequence number
                    return 0
        else:  # Timeout
            print("! TIMEOUT !")
            # Re-transmit packet
            try:
                #sock.sendto(UDP_packet, (UDP_IP, UDP_PORT))
                sock.sendto(UDP_packet, address)
            except socket.error as err_msg:
                print("Socket send error: ", err_msg)
                return -1
            print("rdt_send_file(): Re-sent one message [%d] -> " % (sequence_num_file))

# Our main function.

def main():
    # Register our signal handler for shutting down.

    signal.signal(signal.SIGINT, signal_handler)

    # Create the socket.  We will ask this to work on any interface and to pick
    # a free port at random.  We'll print this out for clients to use.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.settimeout(1000)
    server_socket.bind((UDP_IP, UDP_PORT))
    print('Will wait for client connections at port ' + str(server_socket.getsockname()[1]))
    sel.register(server_socket, selectors.EVENT_READ, accept_client)
    print('Waiting for incoming client connections ...')

    # Keep the server running forever, waiting for connections or messages.

    while (True):
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj,mask)


if __name__ == '__main__':
    main()
