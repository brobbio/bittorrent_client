# bittorrent_client
Command line implementation of a bittorrent client. 

Status: In progress

# Dependencies

Python3

# Content

```torrent_parser.py```: Python script that extracts metadata from torrent files and produces a dictionary with the relevant information as described in the [Bittorrent Protocol Specification](https://wiki.theory.org/BitTorrentSpecification#Metainfo_File_Structure).

```tracker_info.py```: Parses the response of the tracker of a torrent from its 'announce' information.

```connect.py```: Makes a connection to a peer.

