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
from torrent import Torrent


####################################################################
####################################################################
########ESTABLISH A CONNECTION######################################
####################################################################
####################################################################


import struct
import socket
from requests.exceptions import ConnectionError
from torrent_metadata import Metadata
from trackerData import trackerData

class ConnectionToPeer():
    def __init__(self):
        self.peer_id = None
        self.ip = ''
        self.port = 0
        self.connectionEstablished = False
        self.connection = None

    def establish_conn(self, peer, metadata):
        '''Sends handshake to a single peer in the tracker list'''
        #Build the handshake to send
        #Format of handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
        info_hash = hashlib.sha1(bencodepy.encode(metadata.info)).digest()
        pstr = b'BitTorrent protocol'
        fmt = '!B%ds8x20s20s' % len(pstr)
        pstrlen = b'19'
        reserved = b'00000000'

        handshake = struct.pack(fmt, len(pstr), pstr, info_hash, peer_id)

        #Request the list of available peers to tracker
        r = requests.get(url)
        respuesta = parsing(r.content,0)[0]
        peers = respuesta[b'peers']

        #Choose one peer. TODO: How to handle multiple peers at once?
        peer = peers[0]

        #Send handshake
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((peer[b'ip'],peer[b'port']))
        except ConnectionError as e:
             print(e)
             s = "No response"

        self.connection = s
        s.send(handshake)


##################################################################
###AT THIS POINT WE HAVE CONNECTED AND SENT HANDSHAKE TO A PEER###
##################################################################
