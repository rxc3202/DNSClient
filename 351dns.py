#! /usr/bin/python3
"""
Filename: 351dns.py
Author(s): Ryan Cervantes (rxc3202), Daniel Osvath (do3477)
"""
import sys
import socket
import time
from DNSMessage import Message, RCODE, QTYPE

REQUEST_TIMEOUT = 0.01  # timeout per request
TOTAL_TIMEOUT_S = 5  # total timeout for receiving the packet


def dump_packet(encoded_packet):
    """
    Dump a packet in hex form
    :param encoded_packet: the packet in byte encoding
    """
    # convert bytes to hex
    p_hex = " ".join([f"{i:02x}" for i in encoded_packet])  # hex string

    hex_eight_len = 23  # 2 groups of 8 hex values
    block_number = 0

    while p_hex:
        # insert extra space between groups of 8 hex values
        s1 = p_hex[0:hex_eight_len] + " " + p_hex[hex_eight_len:(hex_eight_len * 2 + 1)]
        # ascii value
        s2 = "".join([chr(i) if 32 <= i <= 127 else "." for i in bytes.fromhex(s1)])

        print(f"[{block_number * 16:04x}]  {s1}  {s2}")

        block_number += 1
        p_hex = p_hex[(hex_eight_len * 2 + 2):]


def print_response(res):
    """
    Print the DNS response
    :param res: the response object from the DNS
    """
    responses = res.get_responses()
    for response in responses:
        record_type = Message.net_to_int(response[1])
        if record_type == 1:
            output = "IP\t" + socket.inet_ntoa(response[5])
        else:
            output = QTYPE(record_type).name + "\t" + response[5].decode('utf-8')

        print(output)


def wait_for_packet_with_identifier(packet_id, s):
    """
    Wait for the packet with the given identifier until timout.
    :param packet_id: the identifier of the packet
    :param s: the socket
    """
    s.settimeout(REQUEST_TIMEOUT)
    timeout_start = time.time()

    while time.time() < timeout_start + TOTAL_TIMEOUT_S:
        try:
            (response, address) = s.recvfrom(512)
            res = Message()
            res.decode(response)
            if Message.net_to_int(res.identifier) == packet_id:
                rcode = res.get_bits(res.flags[1], 0, 4)
                if rcode == RCODE.NO_ERROR.value:
                    print_response(res)
                elif rcode == RCODE.NAME_ERROR.value:
                    print("NOTFOUND")
                else:
                    print("ERROR\t" + RCODE(rcode).name)
                return

        except socket.timeout:
            pass

    print("NORESPONSE")


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
        host = ''  # all available interfaces
        s.bind((host, 5555))
        try:
            dump_packet(msg.encode())
            s.sendto(msg.encode(), (server, port))
            wait_for_packet_with_identifier(1337, s)

        except socket.gaierror as e:
            print("ERROR\t" + e.strerror)
        s.close()


if __name__ == '__main__':
    main()
