#!/usr/bin/env python3

from time import sleep
import socket, sys

default_address_dummysmtp = ["", 110]
default_dummysmtp_sleep_time = 0.5

def main(host=default_address_dummysmtp[0], port=default_address_dummysmtp[1], sleep_time=default_dummysmtp_sleep_time):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
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
                sleep(sleep_time)
                sock.close()
                break

if __name__ == "__main__":
    port = None

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if (port < 0) or (port > 65535):
                port = None
        except:
            pass
    if port is None:
        port = default_address_dummysmtp[1]

    print("Starting Dummy SMTP on port " + str(port))
    main(port=port)
