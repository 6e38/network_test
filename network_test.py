# Copyright (c) 2020, Nathan Jenne
# Slow traffic sender/receiver

import signal
import socket
import sys
import time


running = True
direction = 'up'


def serve(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), port))
    server.listen(2)

    print("Listening on port {}".format(port))
    while running:
        connection, addr = server.accept()
        print("Received connection from {}".format(addr))
        if direction == 'up':
            receive_data(connection)
        else:
            send_data(connection)


def connect(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    print("Connecting to {}:{}".format(host, port))
    if direction == 'up':
        send_data(connection)
    else:
        receive_data(connection)


def receive_data(connection):
    print("Receiving data...")
    while running:
        b = connection.recv(1024)
        if len(b) == 0:
            break
        # print(b.decode('UTF-8'))


def send_data(connection):
    print("Sending data...")
    while running:
        connection.send('''This is the data that never ends,
Yes it goes on and on my friend,
Some people started sending it not knowing what it was,
And they'll keep sending it forever just because...
'''.encode('UTF-8'))
        time.sleep(0.1)


def main(argv):
    signal.signal(signal.SIGINT, sig_handler)
    args = argv[1:]
    global direction
    if '--down' in args:
        direction = 'down'
        args.remove('--down')
    if '--up' in args:
        direction = 'up'
        args.remove('--up')
    if '--server' in args:
        args.remove('--server')
        if len(args) >= 1:
            port = int(args[0])
            serve(port)
        else:
            print("Must provide port")
    else:
        if len(args) >= 2:
            host = args[0]
            port = int(args[1])
            connect(host, port)
        else:
            print("Must provide host & port")


def sig_handler(__, _):
    global running
    running = False


if __name__ == "__main__":
    main(sys.argv)
