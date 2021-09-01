import requests
import bencodepy
import urllib
import hashlib
from torrent_metadata import Metadata
from torrent_parser import parsing

class trackerData():
    def __init__(self):
        self.complete = -1
        self.incomplete = -1
        self.interval = -1
        self.mininterval = -1
        self.tracker_id = '-AZ2060-834567891011'
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
            if(b'failure reason' in respuesta.keys()):
                print(respuesta[b'failure reason'].decode('utf-8'))
            if(b'warning message' in respuesta.keys()):
                print(respuesta[b'warning message'].decode('utf-8'))
            else:
                peers = respuesta[b'peers']          #Guardo la lista de peers disponibles
                #TODO: CHECK IF OTHER metadataS HAVE A LIST OF PEERS INSTEAD OF ONE.
                self.complete = respuesta[b'complete']
                self.incomplete = respuesta[b'incomplete']
                self.interval = respuesta[b'interval']
                if b'tracker id' in respuesta.keys():
                    self.tracker_id = respuesta[b'tracker id']
                if type(peers) is list: #Puede ser diccionario o cadena de bytes
                    if(type(peers[0]) is dict):
                        self.peers = peers
                        # peer = peers[0]
                        # peer_id = peer[b'peer id']
                        # ip = peer[b'ip']
                        # port = peer[b'port']
                if type(peers) is bytes :
                    diccio = dict([])
                    j = 0
                    while(j<len(peers)):
                        ip = ''
                        port = ''
                        for i in range(4):
                            ip = ip + '.' + str(peer[j+i])
                        ip = ip[1:]
                        for i in range(2):
                            port = port + str(peer[j+i+4])
                        port = int(port)
                        diccio[b'ip'] = ip
                        diccio[b'port'] = port
                        j = j+6
                    self.peers = diccio

    def __repr__(self):
        return "Complete:"+ str(self.complete) + '\n'+"Incomplete: " + str(self.incomplete) + '\n'+"Comment: "+ str(self.interval + '\n'+"Tracker ID: "+self.tracker_id)
