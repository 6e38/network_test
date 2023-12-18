# Copyright (c) 2020, Nathan Jenne
# Fast traffic sender

import signal
import socket
import sys
import time
from datetime import datetime


running = True
direction = 'up'


def serve(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(3)
    server.bind(('localhost', port))
    # server.bind((socket.gethostname(), port))
    server.listen(2)

    print('Listening on port {}, <ctrl-c> to stop'.format(port))
    while running:
        try:
            connection, addr = server.accept()
        except socket.timeout:
            continue
        print('Received connection from {}'.format(addr))
        if direction == 'up':
            receive_data(connection)
        else:
            send_data(connection)


def connect(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(5)
    try:
        connection.connect((host, port))
    except socket.timeout:
        print('failed to connect to server')
        return
    print('Connecting to {}:{}'.format(host, port))
    if direction == 'up':
        send_data(connection)
    else:
        receive_data(connection)


def receive_data(connection):
    print('Receiving data...')
    bytesReceived = 0
    start = datetime.now()
    while running:
        b = connection.recv(1024)
        if len(b) == 0:
            break
        bytesReceived += len(b)
        # print(b.decode('UTF-8'))
    end = datetime.now()
    delta = end - start
    mbitsPerSecond = (bytesReceived * 8 / 1000000) / delta.seconds
    print(f'bytes received {bytesReceived} in {delta.seconds}\nMbps {mbitsPerSecond}')


def send_data(connection):
    print('Sending data...')
    counter = 0
    while running:
        connection.send('''{}: This is the data that never ends,
Yes it goes on and on my friend,
Some people started sending it not knowing what it was,
And they'll keep sending it forever just because...
'''.format(counter).encode('UTF-8'))
        counter += 1


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
            print('Must provide port')
    else:
        if len(args) >= 2:
            host = args[0]
            port = int(args[1])
            connect(host, port)
        else:
            print('Must provide host & port')


def sig_handler(__, _):
    print('teminating connections')
    global running
    running = False
    time.sleep(3.1)
    print('quitting')
    quit()


if __name__ == '__main__':
    main(sys.argv)
