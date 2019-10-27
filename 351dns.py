#! /usr/bin/python3
"""
Filename: 351dns.py
Author(s): Ryan Cervantes (rxc3202)
"""
import sys
import socket
from DNSMessage import Message

def main():
    if len(sys.argv) != 3:
        print("Usage: {} @<server:port> <name>".format(sys.argv[0]))
        sys.exit(1)
    args = sys.argv[1].replace('@', '').split(':')
    server = args[0]
    port = int(args[1]) if len(args) == 2 else 53
    fqdn = sys.argv[2]

    # Generate the DNS Message
    msg = Message()
    msg.set_identifier(1337)
    msg.set_flags(rd=1)
    msg.set_QDCount(1)
    msg.add_question(fqdn)
    
    # Create socket to read packets from network
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        host = '' # all available interfaces
        s.bind((host, 5555))
        try:
            s.sendto(msg.encode(), (server, port))
            (response, address) = s.recvfrom(512)
            res = Message()
            res.decode(response)
            print(res.get_responses())
            print(res.get_header())
            print(res.encode())
        except socket.gaierror as e:
            print(e)
        s.close()


if __name__ == '__main__':
    main()
