#This is the code where the multi-threaded socket client will be


from torrent_metadata import Metadata
from trackerData import trackerData
from connectionToPeer import ConnectionToPeer
import logging
from piece_downloader import Piece
logger = logging.getLogger(__name__)

TORRENT_SHORTCUT = {
    'ubuntu_nuevo': "./Torrent_examples/ubuntu-23.10-live-server-amd64.iso.torrent"
}

class PieceDownloader:
    def __init__(self, pieces_lengths, fileName):
        self.pieces = [Piece(i, piece_length , f"{fileName}_{i}") for i, piece_length in zip(range(len(pieces_lengths)), pieces_lengths)]
        self.blockRequestSize = 2**14
        self.fileName = fileName

    def write_to_n_piece(self, n, data):

        if n > len(self.pieces) - 1:
            logger.error(f"Piece {n} not in range")
            raise Exception(f"Piece {n} not in range")
        
        self.pieces[n].write_to_piece(data)

class TorrentClient():

    def __init__(self, fileName):
        self.connectionToPeers = []
        self.metaData = None
        self.tracker = None
        self.fileName = fileName

        self.get_peers(self.metaData)
        self.piece_downloader = PieceDownloader(self.metaData.get_pieces_length(), fileName)

    def add_peer(self, peer):
        self.connectionToPeers.append(peer)

    def start_torrent(self):
        self.extract_metadata()
        self.send_announce()
        self.contact_peers()

    def extract_metadata(self):
        try:
            logger.info(f"Extracting metadata from file {self.fileName}")
            self.metaData = Metadata(self.fileName)
        except:
            logger.error(f"Metadata of file could not be extracted")
            exit(1)

    def send_announce(self):
        try:
            logger.info("Connecting to tracker")
            self.tracker = trackerData(self.metaData)
            self.tracker.get_tracker_info()
        except:
            logger.error(f"Could not fetch information from tracker")
            exit(1)

    def contact_peers(self):
        info_hash = self.metaData.get_info_hash()
        logger.info(f"tracker peers: {self.tracker.peers}")

        for peer in self.tracker.peers:
            try:
                conn = ConnectionToPeer(peer)
                conn.send_handshake(info_hash)
                self.connectionToPeers.append(conn)
            except:
                logger.info(f"Could not connect to peer: {conn}")
                continue

    def get_peers(self):
        return self.connectionToPeers
    
    


if __name__ == '__main__':
    torrent = input()

    logging.basicConfig(filename='bittorrent_client.log', level=logging.INFO)
    logger.info('Started')

    file = TORRENT_SHORTCUT[torrent]
    torrent_client = TorrentClient(file)
    torrent_client.start_torrent()

    logger.info('Finished')

