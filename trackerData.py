import requests
import bencodepy
from urllib.parse import quote
import hashlib
from torrent_metadata import Metadata
from torrent_parser import encode_bencoding, decode_bencoding


class trackerData():
    def __init__(self, metadata):
        self.complete = -1
        self.incomplete = -1
        self.interval = -1
        self.mininterval = -1
        self.tracker_id = '-AZ2060-834567891011'
        self.peers = []

        metadata.extract_info()
        self.metadata = metadata

    def get_tracker_info(self):
        url = self.metadata.get_announce()

        #info_hash = hashlib.sha1(bencodepy.encode(metadata.info)).digest()

        percent_encoded = quote(self.metadata.get_info_hash())

        ###Format of peer_id is -AZ2060-LEN12RANDOMNUMBERS. The -..- was taken from the bitmetadata protocol page
        fields = ['peer_id', 'port', 'left', 'uploaded', 'downloaded']
        signature = ['-AZ2060-834567891011', '6881', str(self.metadata.length), '0', '0']

        url = url + '?' + 'info_hash=' + percent_encoded
        for field, signature in zip(fields, signature):
            url = url + '&' + field + '=' + signature

        r = requests.get(url)

        if(r.status_code == 200):
            respuesta = decode_bencoding(r.content, 0)[0]        #Parseo el diccionario con la respuesta del GET

            if b'failure reason' in respuesta.keys():
                print(respuesta[b'failure reason'].decode('utf-8'))
            elif b'warning message' in respuesta.keys():
                print(respuesta[b'warning message'].decode('utf-8'))
            else:
                peers = respuesta[b'peers']          #Guardo la lista de peers disponibles
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
        return f"""Complete: {str(self.complete)}
Incomplete: {str(self.incomplete)}
Interval: {str(self.interval)}
Tracker ID: {self.tracker_id}"""


if __name__ == '__main__':
    
    metadata = Metadata("./Torrent_examples/Okupas [Remasterizado HD 2021] (con música original).torrent")
    
    metadata = Metadata("./Torrent_examples/ubuntu-23.10-live-server-amd64.iso.torrent")
    tracker_data = trackerData(metadata)
    tracker_data.get_tracker_info()

