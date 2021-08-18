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
            s.connect((self.ip, self.port))
            # s.send(handshake)
            # handshake_reply = s.recv(len(handshake))
            # if len(handshake_reply) == len(handshake):
            #     print("Connection to peer successful")
            #     self.connectionEstablished = True
            # else:
            #     print("Connection to peer unsuccessful")
            # print(handshake_reply)
            self.connectionEstablished = True
        except ConnectionError as e:
             print(e)
             s = "No response from peer"

        self.connection = s


    def __repr__(self):
        return "Peer id: "+ str(self.peer_id) + '\n'+ "Ip: " + str((self.ip).decode('utf-8')) + '\n'+"Port: "+ str(self.port) + '\n'+"Connection established: "+ str(self.connectionEstablished)

##################################################################
###AT THIS POINT WE HAVE CONNECTED AND SENT HANDSHAKE TO A PEER###
##################################################################
