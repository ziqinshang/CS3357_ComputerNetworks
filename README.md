# CS3357 ComputerNetworks
## Assignment1: Experience in UDP network simulation, network reliability
#### client.py and server.py needs to be run in different terminals (command windows)
#### In server window: python3 server.py
#### In client window: python3 client.py localhost <portnumber>
##### port number is reported by server.py
## Assignment2: Create a multi-client-single-server chat application with TCP
### Requirements:
- You start by launching your chat server.  It needs to be first as chat clients will need to connect to it to be able to message one another.  When it starts, it picks a random port to listen for clients on, and then reports this port number so that your clients know where to find it.
- When you start a chat client, you provide it the address of the server and a user name for use in the chat system.  On startup, the client will establish a connection with the chat server and register itself with the server.  This way, the server knows the client exists to send messages to it later on.  Multiple clients can be started in this fashion and so the server must support communicating with multiple clients at the same time.
- To send a message, a user will type it at a prompt provided by their chat client.  Each message is composed of a single line of text.  When the user hits enter/return on their keyboard, their client will send this message to the chat server, prefixed with "@username: ", where username is a user name provided during registration.
- When the chat server receives a message from a chat client, the server will broadcast the received message out to every chat client connected and registered at that time, except for the one that originally sent the message.  In this way, every other chat client will receive this message. 
- When a chat client receives a message from the chat server, it will display this message for its user.
- When a chat client ultimately wants to shut down, it notifies the chat server so the chat server can remove it from its list of connected clients.  Likewise, when the chat server shuts down, it notifies all connected clients, so they can disconnect and shut themselves down.  (If there is no chat server, there is no point for the chat clients to stick around.)
### Implementation:
#### In server window: python3 server.py
#### In client window: python3 client.py *username* chat://localhost:*portnumber*
##### port number is reported by server.py, username is chosen by the user himself
## Assignment3: Extension of Assignment2 that supports multiple commands and file transfer
### Requirements:
- Your client and server are run the same as they were in Assignment #2.  (User name and server address as command line options to the client, etc.)
- Your client and server must now support a number of commands to do various things.  These commands all begin with an exclamation mark (!), entered at the prompt of the client.  The first of these commands is "!list".  When entered at the client, it is sent over to the server, and the server responds with a comma separated list of all users online at the moment.
- Your server now keeps track of a "follow list" for each online user.  This is a list of all of the terms the user is following, which can include user names as well. Only messages that contain followed terms are delivered to users; messages are not broadcast everywhere.  When a client sends a message to the server, the server scans the follow list for each online user to determine which user(s) will be forwarded a copy of the message.  The server simply scans each word of a message looking for follow terms, trailing punctuation still results in a match, but otherwise subwords do not count.  For example, suppose user alice is following the term "apple".  A message like "Would you like an apple?" would be forwarded to alice, but a message like "Do you want a pineapple?" would not.
- By default, each user follows themselves.  (So user alice follows @alice, user bob follows @bob, etc.). That way, each user will receive messages containing direct mentions of them.
- There is now also a special reserved username:  "all".  Each user also by default follows @all, so any message containing @all is effectively broadcast to all users.  Users cannot choose to register as the "all" user; attempts to do so should result in an invalid registration response form the server.
- To manage their follow list, a number of commands can be executed by the user.  The first is "!follow?" ... when typed at a prompt at a client, this command is sent to the server, and the server responds with a comma separated list of all follow terms for the user.
- The second is "!follow term", where "term" is another term to follow.  When received at the server, the server adds "term" to the follow list for the user, so that the user receives all messages containing the given term. 
- The last command is "!unfollow term", where "term" is a currently followed term.  On receiving this message, the server removes the term from the list of those followed by the user.  Any term can be unfollowed this way, except for @all and @username for the user.  Attempts to follow a term multiple times, attempts to remove a term not being followed, and attempts to remove terms that cannot be unfollowed should result in an error being returned to the client.  On success, appropriate messages are returned as well. 
- A new "!exit" command must also be supported.  When entered at a client's prompt, the client will be disconnected from the server. 
- The last command is "!attach", or to be more precise "!attach filename terms".  This will send the file named "filename" to users following the given terms or the user sending the message.  This will involve reading the file chunk-by-chunk and sending each chunk to the appropriate recipients until the file is entirely sent.  To tell how much data to send and to receive, you will need to determine the size of the file and communicate that size in sending things.  (Much like the Content-Length header field of HTTP.). Any errors in the process (such as if "filename" does not exist) must be reported to the user.  On receipt of the file, the receiving clients will save it under the same name as what was given to the "!attach" command. 
### Implementation:
#### In server window: python3 server.py
#### In client window: python3 client.py *username* chat://localhost:*portnumber*
##### port number is reported by server.py, username is chosen by the user himself
#### TO TEST !attach functionality:
1. follow the file name you want to get on receiver client by !follow <filename>
2. use !attach command with the form: !attach <filename>
## Assignment4: Replacement of TCP to UDP with RDT
### Requirements:
- You are required to take your TCP-based chat client and server from Assignment #3 and replace its use of TCP with UDP.  In the process, you are to implement a reliable data transfer protocol on top of UDP to ensure that your application can tolerate lost and corrupted packets.  As a result, you will need to provide additional code for error detection, retransmission, and timeouts.
- For this assignment, your chat client and server must support the stop-and-wait reliability protocol (RDT 3.0) discussed in class and in the course textbook. This means that you do not need to buffer more than one outstanding packet at a time. When a packet is sent, you wait for it to be acknowledged before returning to allow the program to send another packet. This means you will need to add a sequence number and acknowledgement fields to data being transmitted, and implement the necessary support functionality as discussed in the lecture materials. 
### Implementation:
#### In server window: python3 server.py
#### In client window: python3 client.py *username* chat://localhost:*portnumber*
##### port number is reported by server.py, username is chosen by the user himself
#### To Start, register first, In the command prompt, type:
#### REGISTER CHAT/1.0
#### To transfer a file from client to another client who is following a <term>:
#### !attachment *filename* *term*
