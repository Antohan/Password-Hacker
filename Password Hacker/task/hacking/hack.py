import sys
import socket


ip_address = sys.argv[1]
port = int(sys.argv[2])
password = sys.argv[3]

with socket.socket() as sock:
    sock.connect((ip_address, port))
    send_data = password.encode()
    sock.send(send_data)
    response = sock.recv(1024)
    data = response.decode()
    print(data)
