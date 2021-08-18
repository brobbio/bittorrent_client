import urllib
import hashlib
import bencodepy
import struct
import socket
from requests.exceptions import ConnectionError
from torrent_parser import parsing
from random import randint
from torrent_metadata import Metadata
from trackerData import trackerData
from connect import ConnectionToPeer

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

m = Metadata()
m.extract_info()

tracker = trackerData()
tracker.get_tracker_info(m)



info_hash = hashlib.sha1(bencodepy.encode(m.info)).digest()
pstr = b'BitTorrent protocol'
fmt = '!B%ds8x20s20s' % len(pstr)
pstrlen = b'19'
reserved = b'00000000'

handshake = struct.pack(fmt, len(pstr), pstr, info_hash, (tracker.tracker_id).encode('utf-8'))

def receive_handshake(handshake, c):
    #s = c.connection
    #s.connect((c.ip, c.port))
    c.connection.sendall(handshake)
    response = c.connection.recv(len(handshake))
    unpacked_response = None
    pstr = b'BitTorrent protocol'
    fmt = '!B%ds8x20s20s' % len(pstr)
    if(not response):
        print("Failed handshake")
    else:
        unpacked_response = struct.unpack(fmt, response)

        # if(unpacked_response[-1]!=tracker.peers[0][b'peer id']):
        #     s.close()
    #TODO: (WHEN SERVING FILES):
        #CLOSE THE CONNECTION IF I RECEIVE A INFO_HASH DIFF FROM THE ONE I'M SERVING
        return unpacked_response

success_list = []

for peer in tracker.peers:
    c = ConnectionToPeer(peer)
    try:
        c.establish_conn(tracker, m)
    except ConnectionResetError or ConnectionRefusedError as e:
        print(e)
        s = "No response from peer"
        continue
    res = receive_handshake(handshake, c)
    success_list.append(res)
    # if not (type(receive_handshake(handshake, c)) is None):
    #     success_list = success_list +1


def msg_parser(msg):
    '''Accepts an unpacked handshake from peer'''
    if msg[1].decode('utf-8')!='BitTorrent protocol' :
        raise ConnectionError('Unknown protocol')
    log.debug('Received handshake from peer')

def construct_msg(type):
    '''The structure of the message is <length_prefix><msg_id><payload>'''
    message_type = -1
    types = ['choke', 'unchoke', 'interested', 'not_interested', 'have', 'bitfield', 'request', 'piece', 'cancel', 'port']
    for n, elmt in enumerate(types):
        if elmt == type:
            message_type = n
            break
    if message_type == -1:
        raise ConnectionError('Unrecognized message')
    length_prefix = len(payload)+1
    fmt = '!LB%ds' % len(payload)
    msg = struct.pack(fmt, length_prefix, message_type, payload)
    return msg

#def send_msg(type, **params):
