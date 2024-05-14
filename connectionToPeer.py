
import requests
import urllib
import hashlib
import bencodepy
import logging 
import logging
logger = logging.getLogger(__name__)
from random import randint
import struct
from bitstring import BitArray
#from torrent import Torrent


#######################################
#######################################
########ESTABLISH A CONNECTION#########
#######################################
#######################################

import socket
from requests.exceptions import ConnectionError
from torrent_metadata import Metadata
from trackerData import trackerData

translate_type = {
    'keep_alive': 0,
    'choke': 1,
    'unchoke': 2,
    'interested': 3,
    'not_interested': 4,
    'have': 5,
    'bitfield': 6,
    'request': 7,
    'piece': 8,
    'cancel': 9
}

class ConnectionToPeer():
    def __init__(self, peer):
        self.peer_id = peer[b'peer id']
        self.ip = peer[b'ip']
        self.port = peer[b'port']
        self.connectionEstablished = False
        self.connection = None
        self.buffer = b''
        self.state = {'handshake_received': False,
                        'connection_failed': False,
                        'am_choking': True,
                        'am_interested': False,
                        'peer_choking': True,
                        'peer_interested': False
        }
        self.available_pieces = b""

    def receive_response(self):
        return self.buffer.decode('utf-8')
    
    def verify_handshake(self, info_hash):

        '''this version's verified handshake only allows 8 reserved bytes to be zero'''
        is_protocol_correct = b"\x13BitTorrent protocol\x00\x00\x00\x00\x00\x00\x00\x00" == self.buffer[:28]
        is_info_hash_correct = info_hash == self.buffer[28:48]
        is_peer_id_correct = self.peer_id == self.buffer[48:68]

        if not is_protocol_correct:
            raise Exception(f"I had to refuse handshake with peer {self.peer_id}. Received non-zeroes in trailing bytes.")

        if not is_info_hash_correct:
            raise Exception(f"I had to refuse handshake with peer {self.peer_id}. Wrong info hash received.")
        
        if not is_peer_id_correct:
            raise Exception(f"I had to refuse handshake with peer {self.peer_id}. Peer id is either invalid or too long.")


        return is_protocol_correct and is_info_hash_correct and is_peer_id_correct
    
    def pack_length(self, payload):
        return struct.pack("<I", len(payload))[::-1]

    def send_keep_alive_msg(self):

        self.connection.sendall(b'\x00\x00\x00\x00')

    def send_choke_msg(self):
        msg = self.construct_msg('choke')

        self.connection.sendall(msg)

    def send_unchoke_msg(self):
        msg = self.construct_msg('unchoke')
    
        self.connection.sendall(msg)

    def send_interested_msg(self):
        msg = self.construct_msg('interested')
    
        self.connection.sendall(msg)

    def send_not_interested_msg(self):
        msg = self.construct_msg('not_interested')
    
        self.connection.sendall(msg)
        
    def send_have_msg(self, piece_index):
        msg = self.construct_msg('have', piece_index)

        self.connection.sendall(msg)

    def send_bitfield_msg(self):
        '''This msg can only be sent right after handshake'''

        bitfield = self.construct_bitfield()

        msg = self.construct_msg('bitfield', bitfield)

        self.connection.sendall(msg)

    def construct_bitfield(self):
        """TODO"""


    def construct_msg(self, type, *payload):
        msg = self.pack_length() + translate_type[type]
        
        for elm in payload:
            msg += elm

        return msg

    def receive_message(self):
        msg = self.buffer 

        length_prefix = msg[:4]
        msg_id = msg[4]
        payload = msg[5:]

        msg_length = int(struct.unpack("<I", length_prefix[::-1])[0])

        if msg_id == "0":
            self.state['peer_choking'] = True

        if msg_id == "1":
            self.state['peer_choking'] = False

        if msg_id == "2":
            self.state['peer_interested'] = True

        if msg_id == "3":
            self.state['peer_interested'] = False

        if msg_id == "4":
            self.state['peer_interested'] = True


    def receive_handshake(self, info_hash):
        handshake = self.buffer

        try:
            self.verify_handshake(info_hash)
        except Exception as e:
            logger.warning(e)
            self.connection.close()
            logger.info(f"Connection with peer {self.peer_id} has been closed due to invalid handshake")

        self.connectionEstablished = True 
        self.buffer = b''



    def send_handshake(self, info_hash):
        logger.info(f"Sending handshake to ip: {self.ip.decode('utf-8')} in port {self.port}")
        HANDSHAKE = b"\x13BitTorrent protocol\x00\x00\x00\x00\x00\x00\x00\x00" + info_hash + b'-AZ2060-834567891011'

        server = (self.ip.decode('utf-8'), self.port, 0, 0)
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)

        try:
            s.connect(server)
            s.sendall(HANDSHAKE)
        except:
            logger.error("Connection to peer failed")
        data = s.recv(1024)

        if data:
            logger.info("Connection to peer has been established")
            logger.info(f"handshake received from peer {self.ip}: {data}")
            self.receive_handshake()
            self.connection = s



    def keep_alive(self):
        '''The keep-alive message is a message with zero bytes, specified with the length prefix set to zero. 
        There is no message ID and no payload. 
        Peers may close a connection if they receive no messages (keep-alive or any other message)
        for a certain period of time, so a keep-alive message must be sent to maintain the connection alive if no command have been sent for a given amount of time. 
        This amount of time is generally two minutes. '''
        msg = b'\x00\x00\x00\x00'
        self.connection.sendall(msg)


    def current_state(self):
        return self.state

    def __repr__(self):
        return f"""Peer id: {self.peer_id}
Ip: {self.ip}"""

if __name__ == '__main__':

    #metaData = Metadata("./Torrent_examples/Okupas [Remasterizado HD 2021] (con música original).torrent")
    #metaData = Metadata("./Torrent_examples/big-buck-bunny.torrent")
    metaData = Metadata("./Torrent_examples/ubuntu-23.10-live-server-amd64.iso.torrent")

    tracker = trackerData(metaData)
    tracker.get_tracker_info()

    info_hash = metaData.get_info_hash()
    print(tracker.peers)
    for peer in tracker.peers:
        try:
            conn = ConnectionToPeer(peer)
            conn.send_handshake(info_hash)
        except:
            print("Could not connect")
            continue