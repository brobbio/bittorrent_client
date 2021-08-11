import urllib
import hashlib
import bencodepy
from torrent_parser import parsing
from random import randint

'''
Messages:

All of the remaining messages in the protocol take the form of <length prefix><message ID><payload>.
The length prefix is a four byte big-endian value. The message ID is a single decimal byte.
The payload is message dependent.

keep-alive: <len=0000>

The keep-alive message is a message with zero bytes, specified with the length prefix set to zero.
There is no message ID and no payload.
Peers may close a connection if they receive no messages
(keep-alive or any other message) for a certain period of time,
so a keep-alive message must be sent to maintain the connection alive if no command have been sent
for a given amount of time.
This amount of time is generally two minutes.

choke: <len=0001><id=0>

The choke message is fixed-length and has no payload.

unchoke: <len=0001><id=1>

The unchoke message is fixed-length and has no payload.

interested: <len=0001><id=2>

The interested message is fixed-length and has no payload.

not interested: <len=0001><id=3>

The not interested message is fixed-length and has no payload.

have: <len=0005><id=4><piece index>

The have message is fixed length.
The payload is the zero-based index of a piece that has just been successfully downloaded and verified via the hash.
'''
