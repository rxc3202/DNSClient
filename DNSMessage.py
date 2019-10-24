#! /usr/bin/python3
"""
Filename: DNSMessage.py
Authors: Ryan Cervantes (rxc3202)
"""

from enum import Enum

class QR(Enum):
    QUERY = 0
    RESPONSE = 1

class OPCODE(Enum):
    QUERY = 0
    IQUERY = 1
    STATUS = 2
    NOTIFY = 4
    UPDATE = 5


class RCODE(Enum):
    NO_ERROR = 0
    FORMAT_ERROR = 1
    SERVER_FAILURE = 2
    NAME_ERROR = 3
    NOT_IMPLEMENTED = 4
    REFUSED = 5
    YX_DOMAIN = 6
    YX_RR_SET = 7
    NX_RR_SET = 8
    NOT_AUTH = 9
    NOT_ZONE = 10


class QTYPE(Enum):
    A = 1
    NS = 2
    CNAME = 5
    SOA = 6
    MX = 15
    TXT = 16
    AAAA = 28


class Message():

    MAX_SIZE = 500

    """ All values stored as byte arrays in big endian"""
    def __init__(self, msgType=QR.QUERY.value, identifier=0, flags=0,
            QDCount=0, ANCount=0, NSCount=0, ARCount=0):
        self.type = Message.int_to_net(msgType)
        self.identifier = bytearray(2)
        self.flags = bytearray(2)
        self.QDCount = bytearray(2)
        self.ANCount = bytearray(2)
        self.NSCount = bytearray(2)
        self.ARCount = bytearray(2)
        self.data = bytearray(b'')

    """
    Will get the range of bits within a given byte where
    start and end are both inclusive. Byte is given as an int,
    0 indexed
    Bit: 0 0 0 0 0 0 0 0 
    Idx: 7 6 5 4 3 2 1 0 
    """
    @classmethod
    def get_bits(cls, byte, start, end=None):
        end = start if not end else end
        mask = int('11111111', 2) # to prevent len(int) > 8
        shift = 7 - end
        return ((byte << shift) & mask) >> (start + shift)


    @classmethod
    def int_to_net(cls, n):
        return bytearray((n).to_bytes(2, "big"))


    @classmethod
    def net_to_int(cls, network_byte):
        return int(network_byte.hex(), 16)

    @classmethod
    def decode(cls, bytearr):
        # Get header information
        ID = byetarr[0:3]
        Flags = bytearr[3:5]
        QDCount = bytearr[5:7]
        ANCount = bytearr[7:9]
        NSCount = bytearr[9:11]
        ARCount = bytearr[11:13] 
        data = bytearr[13:]


    @classmethod
    def encode(cls, msg):
        pass


    def set_flags(self, qr=0, opcode=0, aa=0, tc=0,
            ra=0, rd=0, z=0, rcode=0):
            codes = [
                bin(qr)[2:],
                bin(opcode)[2:].zfill(4),
                bin(aa)[2:],
                bin(tc)[2:],
                bin(ra)[2:],
                bin(rd)[2:],
                bin(0)[2:].zfill(3),
                bin(rcode)[2:].zfill(4)
            ]
            flag_string = ""
            for code in codes:
                flag_string += code
            hex_str = int(flag_string, 2).to_bytes(2, "big")
            self.flags = bytearray(hex_str)
            return self.flags

    def set_QDCount(self, count):
        self.QDCount = bytearray((count).to_bytes(2, "big")) 


    def set_ANCount(self, count):
        self.ANCount = bytearray((count).to_bytes(2, "big"))


    def set_NSCount(self, count):
        self.NSCount = bytearray((count).to_bytes(2, "big"))


    def set_ARCount(self, count):
        self.ARCount = bytearray((count).to_bytes(2, "big"))


    def add_question(self, fqdn, qtype=QTYPE.A, rsrc_class=1):
        question = bytearray(b'')
        # Generate the Question Name field
        qname = bytearray(b'')
        for domain in fqdn.split("."):
            qname += len(domain).to_bytes(1, "big")
            qname += bytes(domain, 'utf-8')
        qname += bytes([0])                   # end the labels
        qname += bytes((4 - len(qname) % 4))  # pad to nearest word
        question += qname
        # Generate Question Type field
        question += bytes(qtype.value.to_bytes(2, "big"))
        # Generate Question Class field
        question += bytes(rsrc_class.to_bytes(2, "big"))
        self.data += question
        return question

    def get_header(self):
        qr=Message.get_bits(self.flags[0], 7)
        opcode=Message.get_bits(self.flags[0], 3, 6)
        aa=Message.get_bits(self.flags[0], 2)
        tc=Message.get_bits(self.flags[0], 1)
        rd=Message.get_bits(self.flags[0], 0)
        ra=Message.get_bits(self.flags[1], 7)
        z=Message.get_bits(self.flags[1], 5, 6)
        rcode=Message.get_bits(self.flags[1], 0, 4)
        flags = (qr, opcode, aa, tc, rd, ra, z, rcode)
        return (
                Message.net_to_int(self.identifier),
                flags,
                Message.net_to_int(self.QDCount),
                Message.net_to_int(self.ANCount),
                Message.net_to_int(self.NSCount),
                Message.net_to_int(self.ARCount)
                )
         

    def get_questions(self):
        pass
        

