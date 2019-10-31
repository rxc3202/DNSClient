# DNSClient

## High Level Approach

The first step was establish the logic of the encoding/decoding of a packet as separate 
from the socket management and network logic of the program. This allows users to easily
create packets separate from the networking aspect of actually sending packets, promoting
portability and an abstraction layer. The DNSMessage file handles
everything that is related to the decoding and decoding of packets. It provides Enums,
Classes and functions in order to construct, manipulate, and encodes to network formatting.
The 351dns.py is the main program that parses the user arguments, handles the networking 
aspect of creating the socket, and sending an initial request to the DNS server.
Before sending, the program dumps the packet using the dump_packet function. 
The program then waits for the packet with the same identifier
as the sent one to arrive or times out after 5 seconds. The response is then printed in 
the required formatting. 

## Challenges Faced`

* Logical bitwise operations in python ore more challenging than in C. 
* When shifting bits, the integer does not stay within an 8bit value, but continues extending.
* Formatting the hex dump to match the writeup. 
* Handling the various error cases. 

## Design Features

* Good logical abstraction for the decoding class via the Message class. 
* Enums are used for readable storage of different error codes
* Structured dump and result print statements.
* Graceful error handling. 

## Testing Process

* Tested locally using @8.8.8.8 www.rit.edu
* Tested on glados using @8.8.8.8 www.rit.edu
