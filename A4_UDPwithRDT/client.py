import socket
import os
import signal
import sys
import sys
import argparse
from urllib.parse import urlparse
import select
import selectors
import struct
import hashlib

# Hard code location of the server.  Not what we'll want to be doing in the assignment,
# but okay for an example like this.

UDP_IP = "localhost"
UDP_PORT = 54321
# Define a maximum string size for the text we'll be sending along.
TIMEOUT = 0.5  # retransmission timeout duration
MAX_STRING_SIZE = 256
CHUNK_SIZE = 1024
CHUNKPACK_SIZE = 1064 # 4 + 4 + 32 + 1024
# Define a constant for our buffer size
TYPE_ACK = 11  # 11 means ACK
BUFFER_SIZE = 1024
sequence_num = 0
sequence_num_file = 0
host = "localhost"
port = 54321
# Selector for helping us select incoming data from the server and messages typed in by the user.

sel = selectors.DefaultSelector()

# Socket for sending messages.

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# User name for tagging sent messages.

user = ''


# Signal handler for graceful exiting.  Let the server know when we're gone.

def signal_handler(sig, frame):
    print('Interrupt received, shutting down ...')
    sys.exit(0)


# Simple function for setting up a prompt for the user.

def do_prompt(skip_line=False):
    if (skip_line):
        print("")
    print("> ", end='', flush=True)


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


# Function to handle incoming messages from server.  Also look for disconnect messages to shutdown and messages for sending and receiving files.

def handle_message_from_server(sock, mask):
    global sequence_num_file
    message, addr = rdt_recv(sock)
    # message = get_line_from_socket(sock)
    words = message.split(' ')
    print()

    # Handle server disconnection.

    if words[0] == 'DISCONNECT':
        print('Disconnected from server ... exiting!')
        sys.exit(0)

    # Handle file attachment request.
    elif words[0] == 'ATTACH2':
        sock.setblocking(True)
        filename = words[1]
        if (os.path.exists(filename)):
            filesize = os.path.getsize(filename)
            header = f'Content-Length: {filesize}\n'
            rdt_send(sock, header)
            with open(filename, 'rb') as file_to_send:
                while True:
                    chunk = file_to_send.read(BUFFER_SIZE)
                    if chunk:
                        rdt_send_file(sock, chunk)
                        sequence_num_file += 1
                    else:
                        break
                sequence_num_file = 0
        else:
            header = f'Content-Length: -1\n'
            sock.send(header.encode())
        sock.setblocking(False)

    # Handle file attachment request.

    elif words[0] == 'ATTACHMENT':
        filename = words[1]
        print(f'Incoming file: {filename}')
        origin = words[4]
        print(origin)
        contentlength = words[6]
        print(contentlength)
        if (words[5] != 'Content-Length:'):
            print('Error:  Invalid attachment header')
        else:
            bytes_read = 0
            bytes_to_read = int(contentlength)
            with open(filename, 'wb') as file_to_write:
                while (bytes_read < bytes_to_read):
                    chunk = rdt_recv_file(sock)
                    print(bytes_read)
                    bytes_read += len(chunk)
                    sequence_num_file += 1
                    file_to_write.write(chunk)
            sequence_num_file = 0

    # Handle regular messages.

    else:
        print(message)
        do_prompt()


# Function to handle incoming messages from server.

def handle_keyboard_input_udp(file, mask):
    line = sys.stdin.readline()
    message = f'@{user}: {line}'
    if line != "\n":
        rdt_send(client_socket, message)
        do_prompt()
    else:
        do_prompt()


# Function to handle incoming messages from server.

def handle_keyboard_input(file, mask):
    line = sys.stdin.readline()
    message = f'@{user}: {line}'
    client_socket.send(message.encode())
    do_prompt()


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


def pack_data_file(data1, seq_num):
    # Our packet is going to contain a sequence number, our data, the size of our data, and a checksum.
    # Note that your packets may need to contain different things.
    data = data1
    size = len(data)
    # We now compute our checksum by building up the packet and running our checksum function on it.
    # Our packet structure will contain our sequence number first, followed by the size of the data,
    # followed by the data itself.  We fix the size of the string being sent ... as we are sending
    # less data, it will be padded with NULL bytes, but we can handle that on the receiving end
    # just fine!
    packet_tuple = (seq_num, size)
    packet_structure = struct.Struct(f'I I')
    packed_data = packet_structure.pack(*packet_tuple) + data
    checksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    # Now we can construct our actual packet.  We follow the same approach as above, but now include
    # the computed checksum in the packet.
    packet_tuple = (seq_num, size, checksum)
    UDP_packet_structure = struct.Struct(f'I I 32s')
    UDP_packet = UDP_packet_structure.pack(*packet_tuple) + data
    return UDP_packet


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

def rdt_send(sock, data1):
    # Our packet is going to contain a sequence number, our data, the size of our data, and a checksum.
    # Note that your packets may need to contain different things.
    global sequence_num
    global host
    global port
    UDP_packet = pack_data(data1, sequence_num)
    # Finally, we can send out our packet over UDP and hope for the best.
    #sock.sendto(UDP_packet, (UDP_IP, UDP_PORT))
    sock.sendto(UDP_packet, (host, port))
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
                    # sequence_num ^= 1  # Flip sequence number
                    return 0
        else:  # Timeout
            print("! TIMEOUT !")
            # Re-transmit packet
            try:
                #sock.sendto(UDP_packet, (UDP_IP, UDP_PORT))
                sock.sendto(UDP_packet, (host, port))
            except socket.error as err_msg:
                print("Socket send error: ", err_msg)
                return -1
            print("rdt_send(): Re-sent one message [%d] -> " % (sequence_num))


# Function to receive data in UDP
def rdt_recv(sock):
    global sequence_num
    global host
    global port
    recv_expected_data = False
    while not recv_expected_data:  # Repeat until received expected DATA
        try:
            received_packet, addr = sock.recvfrom(1024)
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
            print("rdt_recv(): Received [wrong seq_num (%d)] Keep waiting for ACK [%d]" % (
            received_sequence, sequence_num))
            not_ack = make_ack(1 - sequence_num)
            try:
                sock.sendto(not_ack,addr)
            except socket.error as err_msg:
                print("rdt_recv(): Error in ACK-ing corrupt/wrong data packet: " + str(err_msg))
                return -1
        elif received_sequence == sequence_num:
            print("rdt_recv(): Received expected DATA [%d]" % (received_sequence))
            # print("Packet received from:", addr)
            # print('Received and computed checksums match, so packet can be processed')
            received_text = received_data[:received_size].decode()
            #print(f'{received_text}')
            ack_msg = make_ack(sequence_num)
            try:
                # sock.sendto(ack_msg, (UDP_IP, UDP_PORT))
                sock.sendto(ack_msg, addr)
            except socket.error as err_msg:
                print("rdt_recv(): Error in ACK-ing expected data: " + str(err_msg))
                return b''
            print("rdt_recv(): Sent expected ACK [%d]" % received_sequence)
            # received_sequence ^= 1  # Flip seq num
            return received_text, addr


def rdt_send_file(sock, data1):
    # Our packet is going to contain a sequence number, our data, the size of our data, and a checksum.
    # Note that your packets may need to contain different things.
    global sequence_num_file
    global host
    global port
    UDP_packet = pack_data_file(data1, sequence_num_file)
    # Finally, we can send out our packet over UDP and hope for the best.
    #sock.sendto(UDP_packet, (UDP_IP, UDP_PORT))
    sock.sendto(UDP_packet, (host, port))
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
                sock.sendto(UDP_packet, (host, port))
            except socket.error as err_msg:
                print("Socket send error: ", err_msg)
                return -1
            print("rdt_send_file(): Re-sent one message [%d] -> " % (sequence_num_file))


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

# Our main function.

def main():
    global user
    global client_socket
    global sequence_num
    global port
    global host

    # Register our signal handler for shutting down.

    signal.signal(signal.SIGINT, signal_handler)

    # Check command line arguments to retrieve a URL.

    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="user name for this user on the chat service")
    parser.add_argument("server", help="URL indicating server location in form of chat://host:port")
    parser.add_argument('-f', '--follow', nargs=1, default=[], help="comma separated list of users/topics to follow")
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
    follow = args.follow
    sel.register(client_socket, selectors.EVENT_READ, handle_message_from_server)
    sel.register(sys.stdin, selectors.EVENT_READ, handle_keyboard_input_udp)
    # Prompt the user before beginning.

    # do_prompt()

    # Now do the selection.

    while (True):
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    main()
