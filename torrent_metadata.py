import requests
import bencodepy
import urllib
import hashlib
from torrent_parser import encode_bencoding, decode_bencoding, create_info_hash
from math import ceil
import time

class Metadata():
    '''Contains the metadata of a torrent'''
    def __init__(self, file):
        self.file = file
        self.is_private = 0
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
        self.single_file_mode = True

        #Info in single file mode
        self.name = ''
        self.length = 0
        self.md5sum = None #str

        #Info in multiple file mode
        self.directory_name = ''
        self.files = [] #List of dictionaries, each of which has keys
                            #(length: int, md5sum: str, bencoded dict with directory )


    def get_announce(self):
        return self.announce
    
    def get_info_hash(self):
        return self.info_hash
    
    def get_pieces_lengths(self):
        pieces_lengths = [self.piece_length for i in range(len(self.pieces)-1)]

    def get_nmb_pieces(self):
        return self.pieces

    def extract_info(self):
        data = open(self.file, "rb").read()

        try:
            torrent_info = decode_bencoding(data, 0)[0]
        except:
            raise Exception("Torrent metadata could not be extracted.")
        create_info_hash(torrent_info)

        if b'files' in torrent_info[b'info'].keys():
            self.single_file_mode = False

        #Time of creation
        self.creation_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(torrent_info[b'creation date']))
        self.announce = torrent_info[b'announce'].decode('utf-8')

        announce_list = []
        for e in torrent_info[b'announce-list']:
            sub_list = []
            for el in e:
                sub_list.append(el.decode('utf-8'))
            announce_list.append(sub_list)

        self.announce_list = announce_list
        self.comment = torrent_info[b'comment'].decode('utf-8')
        self.created_by = torrent_info[b'created by'].decode('utf-8')
        self.info = torrent_info[b'info']
        if b'private' in torrent_info[b'info'].keys():
            self.is_private = int(torrent_info[b'info'][b'private'])

        self.info_hash = torrent_info[b'info_hash']
        diccio_info = torrent_info[b'info']
        self.name = diccio_info[b'name'].decode('utf-8')

        if self.single_file_mode:
            self.length = diccio_info[b'length']
            if b'piece length' in diccio_info.keys():
                self.piece_length = diccio_info[b'piece length']
            if b'pieces' in diccio_info.keys():
                self.pieces = diccio_info[b'pieces']
            if b'md5sum' in diccio_info.keys():
                self.md5sum = diccio_info[b'md5sum']
            self.numberOfPieces = ceil(self.length // self.piece_length)
        else:
            self.directory_name = diccio_info[b'name'].decode('utf-8')
            self.files = diccio_info[b'files']

    def files_print(self):
        file_print_output = '\n\t\t'
        for file in self.files:
            file_print_output += f"""\t Path: {'/'.join([path_chunk.decode('utf-8') for path_chunk in file[b'path']])}
                    \t Size: {file[b'length']} bytes
                    \t md5sum: {file[b'md5sum'] if b'md5sum' in file.keys() else ''}
                    -----------------------------------
                """
        return file_print_output

    def __repr__(self):
        toPrint = f"""
            Created by: {self.created_by} 
            Creation date: {self.creation_date} 
            Announce: {self.announce} 
            Is Single File: {self.single_file_mode} 
            Piece length: {self.piece_length} 
            File Hash: {self.info_hash} 
            Is Private: {self.is_private}
            Comment: {self.comment} 
            Tracker list: {self.announce_list}
        """
        if self.single_file_mode:
            toPrint += f"""\tFile name: {self.name}
                    Total file size: {self.length} 
                    Pieces: {self.numberOfPieces} 
                    md5sum: {self.md5sum}
                    """
        else:
            toPrint += f"""\tDirectory: {self.name}
                Files: {self.files_print()}
                """
        return toPrint


if __name__ == "__main__":
    metaData = Metadata("./Torrent_examples/Okupas [Remasterizado HD 2021] (con música original).torrent")
    metaData = Metadata("./Torrent_examples/big-buck-bunny.torrent")
    metaData = Metadata("./Torrent_examples/ubuntu-21.04-desktop-amd64.iso.torrent")
    metaData.extract_info()
    print(metaData)