import requests
import urllib
import hashlib
import bencodepy
import logging 
import logging
logger = logging.getLogger(__name__)
from random import randint
import struct


class Piece:
    def __init__(self, piece_index, piece_length ,fileName):
        self.piece_index = piece_index 
        self.piece_length = piece_length
        self.curr_offset = 0
        self.fileName = fileName
        self.complete = False

    def write_to_piece(self, data):

        with open(self.fileName, "r+b") as f:
            try:
                f.seek(self.curr_offset) #write with offset
                f.write(data) #careful: if offset is way past the end of the file, it will fill all with \00
            except:
                logger.error(f"Error writing to file {self.fileName}")

        self.curr_offset += len(data) #update current offset to file

        self.check_piece_complete()

    def check_piece_complete(self):
        if self.curr_offset >= self.piece_length:
            self.complete = True    

    def is_piece_complete(self):
        return self.complete