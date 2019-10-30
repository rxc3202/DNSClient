# DNSClient

## High Level Approach

The first step was establish the logic of the encoding/decoding of a packet as separate 
from the socket management and network logic of the program. The DNSMessage class handles
everything that is related to the deconding and ecoding of DNS packets, both for sending
and receiving. The 351dns.py is the main program that parses the user arguments and makes 
an initial request to the DNS server. Before sendind, the program dumps the packet using
the dump_packet function. The program then waits for the packet with the same identifier
as the sent one to arrive or times out after 5 seconds. The response is then printed in 
the required formatting. 

## Challenges Faced

* Logical bitwise operations in python ore more challenging than in C. 
* Formatting the hex dump to match the writeup. 
* Handling the various error cases. 

## Design Features

* Good logical abstraction for the decoding class.
* Structured dump and result print statements.
* Graceful error handling. 

## Testing Process

* 
