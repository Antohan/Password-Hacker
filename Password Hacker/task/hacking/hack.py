import sys
import socket
import itertools

address = (sys.argv[1], int(sys.argv[2]))


def generate_password():
    index = 1
    while True:
        symbols = 'abcdefghijklmnopqrstuvwxyz0123456789'
        yield from itertools.product(symbols, repeat=index)
        index += 1


with socket.socket() as sock:
    sock.connect(address)

    for p in generate_password():
        password = "".join(p)
        sock.send(password.encode())

        response = sock.recv(1024).decode()
        if response == 'Connection success!':
            print(password)
            break
        if response == 'Wrong password!':
            continue
        if response == 'Too many attempts':
            print(response)
            break
