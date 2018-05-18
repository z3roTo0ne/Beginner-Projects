import socket
import threading
import os

# A typical sequence of a socket connection.
# 1 - Create socket
# 2 - Bind the Socket to an IP and Port
# 3 - Instruct the OS to accept connections as per specifications above.
# 4 - Instruct the OS to receive-send data via the sockets.
# 5 - Close Socket when it is not needed any longer.


class Caller:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.s = socket.socket()
        self.s.connect((host, port))
        print('Connected to', host)

    def receive(self):
        while True:
            received_message = self.s.recv(1024).decode('utf-8')
            if len(received_message) > 0:
                if received_message == 'quit':
                    self.terminate()
                else:
                    print('Receiver: ' + received_message)

    def send(self):
        while True:
            q = input()
            if q == 'quit':
                self.s.send(str.encode(q))
                self.terminate()
            else:
                self.s.send(str.encode(q))

    def terminate(self):
        self.s.close()
        os._exit(0)


class Receiver:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.s = socket.socket()
        self.s.bind((host, port))
        self.s.listen(1)

        print('[Waiting for connection...]')
        self.c, address = self.s.accept()

        print('Got connection from', address)

    def receive(self):
        while True:
            received_message = self.c.recv(1024).decode('utf-8')
            if len(received_message) > 0:
                if received_message == 'quit':
                    self.terminate()
                else:
                    print('Caller: ' + received_message)

    def send(self):
        while True:
            q = input()
            if q == 'quit':
                self.c.send(str.encode(q))
                self.terminate()
            else:
                self.c.send(str.encode(q))

    def terminate(self):
        self.c.close()
        self.s.close()
        os._exit(0)


def main():
    caller_or_receiver = input('Enter 1 if you want to call and 2 if you want to receive: ')

    if caller_or_receiver == '1':
        host = input('Enter host IP: ')
        port = int(input('Enter listening Port: '))

        caller_instance = Caller(host, port)

        thread = threading.Thread(target=Caller.receive, args=(caller_instance,))
        thread.daemon = True
        thread.start()

        Caller.send(caller_instance)

    elif caller_or_receiver == '2':
        host = input('Enter host IP: ')
        port = int(input('Enter listening Port: '))

        receiver_instance = Receiver(host, port)

        thread = threading.Thread(target=Receiver.receive, args=(receiver_instance,))
        thread.daemon = True
        thread.start()

        Receiver.send(receiver_instance)

    else:
        print('Input Error please try again')
        main()


main()
