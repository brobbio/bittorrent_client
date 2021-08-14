import requests
import bencodepy
import urllib
import hashlib
from torrent_metadata import Metadata
from torrent_parser import parsing
class trackerData():
    def __init__(self):
        self.complete = 0
        self.incomplete = 0
        self.interval = 0
        self.peers = []

    def get_tracker_info(self, metadata):
        url = metadata.announce

        info_hash = hashlib.sha1(bencodepy.encode(metadata.info)).digest()

        percent_encoded = urllib.parse.quote(info_hash)

        ###Format of peer_id is -AZ2060-LEN12RANDOMNUMBERS. The -..- was taken from the bitmetadata protocol page
        fields = ['peer_id', 'port', 'left', 'uploaded', 'downloaded']
        signature = ['-AZ2060-834567891011', '6881', str(metadata.length), '0', '0']

        url = url + '?' + 'info_hash=' + percent_encoded
        for field, signature in zip(fields, signature):
            url = url + '&' + field + '=' + signature

        r = requests.get(url)

        if(r.status_code == 200):
            respuesta = parsing(r.content, 0)[0]        #Parseo el diccionario con la respuesta del GET
            peers = respuesta[b'peers']          #Guardo la lista de peers disponibles
            #TODO: CHECK IF OTHER metadataS HAVE A LIST OF PEERS INSTEAD OF ONE.
            self.complete = respuesta[b'complete']
            self.incomplete = respuesta[b'incomplete']
            self.interval = respuesta[b'interval']
            if(type(peers) is list): #Puede ser diccionario o cadena de bytes
                if(type(peers[0]) is dict):
                    self.peers = peers
                    # peer = peers[0]
                    # peer_id = peer[b'peer id']
                    # ip = peer[b'ip']
                    # port = peer[b'port']
            if(type(peers) is bytes):
                ip = ''
                port = ''
                for i in range(4):
                    ip = ip + '.' + str(peer[i])
                ip = ip[1:]
                for i in range(2):
                    port = port + str(peer[i+4])
                port = int(port)
