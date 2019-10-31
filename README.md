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

## Challenges Faced

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

We tested the following nameservers and urls for successful functionality. For each of these the program produced the expected correct result of the lookup. 

### Tested locally using 
* @8.8.8.8 www.rit.edu
* @8.8.8.8 www.google.com
* @8.8.8.8 www.apple.com
* @8.8.8.8 www.yandex.ru
* @8.8.8.8 www.index.hu

* @129.21.3.17 www.rit.edu
* @129.21.3.17 www.google.com
* @129.21.3.17 www.apple.com
* @129.21.3.17 www.yandex.ru
* @129.21.3.17 www.index.hu

* @129.21.4.18 www.rit.edu
* @129.21.4.18 www.google.com
* @129.21.4.18 www.apple.com
* @129.21.4.18 www.yandex.ru
* @129.21.4.18 www.index.hu

### Tested on Glados using
* @8.8.8.8 www.rit.edu
* @8.8.8.8 www.google.com
* @8.8.8.8 www.apple.com
* @8.8.8.8 www.yandex.ru
* @8.8.8.8 www.index.hu

* @129.21.3.17 www.rit.edu
* @129.21.3.17 www.google.com
* @129.21.3.17 www.apple.com
* @129.21.3.17 www.yandex.ru
* @129.21.3.17 www.index.hu

* @129.21.22.218 www.rit.edu
* @129.21.22.218 www.google.com
* @129.21.22.218 www.apple.com
* @129.21.22.218 www.yandex.ru
* @129.21.22.218 www.index.hu

### Testing NORESPONSE
We also tested an expected no response message by using an invalid nameserver with a url for ex. @129.21.5.19 www.rit.edu. The program produced the NORESPONSE message as expected.
