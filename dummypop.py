#!/usr/bin/env python3

import socket, signal, sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 110))
s.listen(1)

# Avoid locking up on windows
signal.signal(signal.SIGINT, lambda *_: sys.exit())
s.settimeout(0.1)

while True:
    try:
        sock, addr = s.accept()
    except TimeoutError:
        continue
    sock.send(b"+OK\r\n")
    while True:
        msg = sock.recv(1024).decode()
        if not msg:
            break
        print(msg)

        if msg.startswith("USER"):
            sock.send(b"+OK\r\n")
        if msg.startswith("PASS"):
            sock.send(b"+OK\r\n")
        if msg.startswith("STAT"):
            sock.send(b"+OK 0 0\r\n")
        if msg.startswith("QUIT"):
            sock.send(b"+OK\r\n")
            sock.close()
            break
