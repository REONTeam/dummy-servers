#!/usr/bin/env python3

from time import sleep
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 110))
s.listen(10)

while True:
    sock, addr = s.accept()
    sock.send(b"+OK\r\n")
    while True:
        msg = sock.recv(1024).decode()
        if msg != "":
            print(msg)

        if msg.startswith("USER"):
            sock.send(b"+OK\r\n")
        if msg.startswith("PASS"):
            sock.send(b"+OK\r\n")
        if msg.startswith("STAT"):
            sock.send(b"+OK 0 0\r\n")
        if msg.startswith("QUIT"):
            sock.send(b"+OK bye\r\n")
            sleep(0.5)
            sock.close()
            break
