#############################GET Requests in python#############################

import requests


#####EJEMPLO#####

r = requests.get('http://xkcd.com/1906/')

----------> r.status_code : devuelve el código de estado del request
----------> r.headers : diccionario con info del request
----------> r.text : código HTML de la página


####BAJAR UNA IMAGEN####

----------> import os
----------> receive = requests.get('https://imgs.xkcd.com/comics/making_progress.png')
----------> with open(r'nueva_imagen.png', 'wb') as f:  #Escribe en
---------->     f.write(receive.content)

r = requests.get('udp://tracker.leechers-paradise.org:6969?info_hash=')


##################################################################
##################################################################
##################################################################

import urllib
import hashlib

url = torrent[b'announce'].decode('utf-8')

info_hash = hashlib.sha1(bencodepy.encode(torrent[b'info'])).digest()

percent_encoded = urllib.parse.quote(info_hash)

url = url + '?' + 'info_hash=' + percent_encoded

r = requests.get(url)

if(r.status_code == 200):
    respuesta = parsing(r.content, 0)[0]        #Parseo el diccionario con la respuesta del GET
    peer = respuesta[b'peers']          #Guardo la lista de peers disponibles
    #TODO: CHECK IF OTHER TORRENTS HAVE A LIST OF PEERS INSTEAD OF ONE.
    if(type(peer) is dict): #Puede ser diccionario o cadena de bytes
        peer_id = peer[b'peer id']
        ip = peer['id']
        port = peer['port']
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
########ESTABLECER CONEXION A PARES#################################
####################################################################
####################################################################


import socket
from requests.exceptions import ConnectionError

#Create the socket to connect to peer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Make the connection
try:
    s.connect((ip, port))
except ConnectionError as e:
    print(e)
    s = "No response"

################################################
##################################################
########HANDSHAKE#################################
##################################################
##################################################
