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

data = open("./Torrent_examples/ubuntu-21.04-desktop-amd64.iso.torrent", "rb").read()
torrent = parsing(data, 0)[0]

url = torrent[b'announce'].decode('utf-8')

info_hash = hashlib.sha1(bencodepy.encode(torrent[b'info'])).digest()

percent_encoded = urllib.parse.quote(info_hash)

###Format of peer_id is -AZ2060-LEN12RANDOMNUMBERS. The -..- was taken from the bittorrent protocol page
fields = ['peer_id', 'port', 'left', 'uploaded', 'downloaded']
signature = ['-AZ2060-834567891011', '6881', str(torrent[b'info'][b'length']), '0', '0']

url = url + '?' + 'info_hash=' + percent_encoded
for field, signature in zip(fields, signature):
    url = url + '&' + field + '=' + signature

r = requests.get(url)

if(r.status_code == 200):
    respuesta = parsing(r.content, 0)[0]        #Parseo el diccionario con la respuesta del GET
    peers = respuesta[b'peers']          #Guardo la lista de peers disponibles
    #TODO: CHECK IF OTHER TORRENTS HAVE A LIST OF PEERS INSTEAD OF ONE.
    if(type(peers) is list): #Puede ser diccionario o cadena de bytes
        if(type(peers[0]) is dict):
            peer = peers[0]
            peer_id = peer[b'peer id']
            ip = peer[b'ip']
            port = peer[b'port']
    if(type(peer) is bytes):
        ip = ''
        port = ''
        for i in range(4):
            ip = ip + '.' + str(peer[i])
        ip = ip[1:]
        for i in range(2):
            port = port + str(peer[i+4])
        port = int(port)

####################################################################
####################################################################
########ESTABLISH A CONNECTION######################################
####################################################################
####################################################################


import struct
import socket
from requests.exceptions import ConnectionError

def establish_conn(url):
    '''Sends handshake to a single peer in the tracker list'''
    #Build the handshake to send
    #Format of handshake: <pstrlen><pstr><reserved><info_hash><peer_id>
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
    s.send(handshake)
    response = s.recv(len(handshake))
    if(not response):
        print("Failed handshake")
    else:
        unpacked_response = struct.unpack(fmt, response)

    if(unpacked_response[-1]!=respuesta[b'peers'][0][b'peer id']):
        s.close()
    #TODO: (WHEN SERVING FILES):
        #CLOSE THE CONNECTION IF I RECEIVE A INFO_HASH DIFF FROM THE ONE I'M SERVING
    return s

conn = establish_conn(url)

##################################################################
###AT THIS POINT WE HAVE CONNECTED AND SENT HANDSHAKE TO A PEER###
##################################################################
