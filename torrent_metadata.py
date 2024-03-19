import requests
import bencodepy
import urllib
import hashlib
from torrent_parser import parsing
from math import ceil
import time

class Metadata():
    '''Contains the metadata of a torrent'''
    def __init__(self):
        self.announce = ''
        self.announce_list = []
        self.comment = ''
        self.created_by = ''
        self.creation_date = 0
        self.encoding = ''
        self.piece_length = 0
        self.pieces = 0
        self.private = None
        self.info = {}
        self.info_hash = ''
        self.single_file_mode = False

        #Info in single file mode
        self.name = ''
        self.length = 0
        self.md5sum = None #str

        #Info in multiple file mode
        self.directory_name = ''
        self.files = [] #List of dictionaries, each of which has keys
                            #(length: int, md5sum: str, bencoded dict with directory )


    def extract_info(self, file = "./Torrent_examples/ubuntu-21.04-desktop-amd64.iso.torrent"):
        data = open(file, "rb").read()
        torrent = parsing(data, 0)[0]

        if b'pieces' in torrent[b'info'].keys():
            self.single_file_mode = True

        #Time of creation
        self.creation_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(torrent[b'creation date']))
        self.announce = torrent[b'announce'].decode('utf-8')
        announce_list = []
        for e in torrent[b'announce-list']:
            for el in e:
                announce_list.append(el.decode('utf-8'))
        self.announce_list = announce_list
        self.comment = torrent[b'comment'].decode('utf-8')
        self.created_by = torrent[b'created by'].decode('utf-8')
        self.info = torrent[b'info']

        diccio = torrent[b'info']
        self.info_hash = self.encode_sha1()
        if self.single_file_mode:
            self.name = diccio[b'name'].decode('utf-8')
            self.length = diccio[b'length']
            if b'piece length' in diccio.keys():
                self.piece_length = diccio[b'piece length']
            if b'pieces' in diccio.keys():
                self.pieces = diccio[b'pieces']
            if b'md5sum' in diccio.keys():
                self.md5sum = diccio[b'md5sum']
            else: ''
        else:
            self.directory_name = diccio[b'name'].decode('utf-8')
            self.files = diccio[b'files']
        self.numberOfPieces = ceil(self.length // self.piece_length)

    def encode_sha1(self):
        sha_1 = hashlib.sha1()
        print(self.info)
        sha_1.update(self.info)
        return sha_1.digest()

    def __repr__(self):
        toPrint = f"""
                Name: {self.name} 
                Total file size: {self.length} 
                Created by: {self.created_by} 
                Creation date: {self.creation_date} 
                Announce: {self.announce} 
                Is Single File: {self.single_file_mode} 
                Piece length: {self.piece_length} 
                Pieces: {self.numberOfPieces} 
                File Hash: {self.info_hash} 
                Comment: {self.comment} 
                Tracker list: {', '.join(self.announce_list)}
                """
        return toPrint


if __name__ == "__main__":
    metaData = Metadata()
    metaData.extract_info()
    print(metaData)