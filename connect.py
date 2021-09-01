#############################GET Requests in python#############################

import requests


#####EJEMPLO#####

#r = requests.get('http://xkcd.com/1906/')

#----------> r.status_code : devuelve el código de estado del request
#----------> r.headers : diccionario con info del request
#----------> r.text : código HTML de la página


####BAJAR UNA IMAGEN####

#----------> import os
#----------> receive = requests.get('https://imgs.xkcd.com/comics/making_progress.png')
#----------> with open(r'nueva_imagen.png', 'wb') as f:  #Escribe en
#---------->     f.write(receive.content)

#r = requests.get('udp://tracker.leechers-paradise.org:6969?info_hash=')


##################################################################
##################################################################
##################################################################

import urllib
import hashlib
import bencodepy
from torrent_parser import parsing
from random import randint
#from torrent import Torrent


#######################################
#######################################
########ESTABLISH A CONNECTION#########
#######################################
#######################################


import struct
import socket
from requests.exceptions import ConnectionError
from torrent_metadata import Metadata
from trackerData import trackerData

m = Metadata()
m.extract_info()

tracker = trackerData()
tracker.get_tracker_info(m)

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

    def establish_conn(self, tracker, metadata):
        '''Sends handshake to a single peer in the tracker list'''
        #Build the handshake to send
        #Format of handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
        info_hash = hashlib.sha1(bencodepy.encode(metadata.info)).digest()
        pstr = b'BitTorrent protocol'
        fmt = '!B%ds8x20s20s' % len(pstr)
        pstrlen = b'19'
        reserved = b'00000000'

        handshake = struct.pack(fmt, len(pstr), pstr, info_hash, self.peer_id)

        #Send handshake
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            print("Trying...")
            s.connect((self.ip, self.port))
            print("Connected")
            s.sendall(handshake)
            self.buffer = s.recv(68)
            self.connectionEstablished = True
        except socket.timeout:
            print("Failed: Connection timeout")
            self.buffer = b"Connection Timeout"
        except ConnectionError as e:
            print(e)
            s = "No response from peer"

        self.connection = s

    def receive_handshake(self):
        '''Receives handshake from recipient once a connection
        has been established'''
        res = {}
        if self.connectionEstablished:
            if self.buffer:
                pstr = b'BitTorrent protocol'
                fmt = '!B%ds8x20s20s' % len(pstr)
                handshake_received = self.buffer
                decoding = struct.unpack(fmt, handshake_received)
                res['pstr'] = decoding[1].decode('utf-8')
                res['info_hash'] = decoding[2]
                res['peer_id'] = decoding[3]
                if res['pstr']!='BitTorrent protocol':
                    print("Unrecognized protocol. Closing connection to peer.")
                    self.connection.close()
                self.handshake_received = True

        else:
            print('Failed handshake. No connection was established')
        return res

    def __repr__(self):
        return "Peer id: "+ str(self.peer_id) + '\n'+ "Ip: " + str((self.ip).decode('utf-8')) + '\n'+"Port: "+ str(self.port) + '\n'+"Connection established: "+ str(self.connectionEstablished)

    def msg_parser(self, msg):
        '''Accepts an unpacked handshake from peer'''
        if msg[1].decode('utf-8')!='BitTorrent protocol' :
            raise ConnectionError('Unknown protocol')
        log.debug('Received handshake from peer')

    def construct_msg(self, type, **params):
        '''The structure of the message is <length_prefix><msg_id><payload>'''
        message_type = -1
        types = ['choke', 'unchoke', 'interested', 'not_interested', 'have', 'bitfield', 'request', 'piece', 'cancel', 'port']
        for n, elmt in enumerate(types):
            if elmt == type:
                message_type = n
                break
        if message_type == -1:
            raise ConnectionError('Unrecognized message')
        if message_type == 6: #If the message is of 'request' type
            payload = struct.pack('!LLL', params['index'], params['begin'], params['length'])

        length_prefix = len(payload)+1
        fmt = '!LB%ds' % len(payload)
        msg = struct.pack(fmt, length_prefix, message_type, payload)
        return msg

    def recv_msg(self, msg):
        '''Receive individual messages from peer'''
        if self.state['handshake_received']:
            while msg:

        else:



    def send_msg(self, type):
        '''Send message to peer'''
        if type == 'request':
            if self.state['am_choking']:
                print('Attempted to request from a choked peer')
        msg = construct_msg()

    def download(self):
        '''Continue requesting blocks of the file'''

##################################################################
###AT THIS POINT WE HAVE CONNECTED AND SENT HANDSHAKE TO A PEER###
##################################################################
