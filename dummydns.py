#!/usr/bin/env python3

import socket, struct

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", 53))

def query(name, qtype):
    # Put custom domain names here
    ip = []
    if qtype == 1:  # A (ipv4)
        if name == "example.com":
            ip = [93, 184, 216, 34]
        else:
            ip = [127, 0, 0, 1]
    elif qtype == 28:  # AAAA (ipv6)
        if name == "example.com":
            ip = [0x26, 0x06, 0x28, 0x00, 0x02, 0x20, 0x00, 0x01,
                    0x02, 0x48, 0x18, 0x93, 0x25, 0xc8, 0x19, 0x46]
        else:
            ip = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]
    print(name, "=", ip)
    return bytes(ip)

def make_name(string):
    res = bytearray()
    for x in string.split("."):
        res.append(len(x))
        res += x.encode()
    res.append(0)
    return bytes(res)

def read_name(data, offs):
    res = ""
    while True:
        len = data[offs]
        offs += 1
        if not len:
            break
        if res:
            res += "."
        res += data[offs:offs+len].decode()
        offs += len
    return res, offs

while True:
    mesg, addr = s.recvfrom(512)
    id, flags, qdcount, ancount, nscount, arcount = struct.unpack_from("!HHHHHH", mesg, 0)

    # Make sure we're receiving a normal query
    if (flags & 0xFE8F) != 0:
        continue
    if qdcount == 0:
        continue

    # Make result flags
    resflags = 0x8000
    # If recursion is desired, set it as available
    if flags & 0x0100:
        resflags |= 0x0180

    # Read first query section
    qname, offs = read_name(mesg, 12)
    qtype, qclass = struct.unpack_from("!HH", mesg, offs)
    if qclass != 1 or (qtype != 1 and qtype != 28):
        continue
    resname = make_name(qname)
    resdata = query(qname, qtype)

    # Encode result
    res = bytearray()
    res += struct.pack("!HHHHHH", id, resflags, 1, 1, 0, 0)
    res += resname
    res += struct.pack("!HH", qtype, qclass)
    res += b'\xc0\x0c'
    res += struct.pack("!HHIH", qtype, qclass, 0, len(resdata))
    res += resdata
    s.sendto(res, addr)
