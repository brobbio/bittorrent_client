import socket
import threading
import logging
from queue import Queue
import threading
from time import time

log = logging.getLogger(__name__)

class connectionManager:
    '''This class manages the main loop'''
    def __init__(self):
        self.connections = []
        self.is_loop_active = False

    def start_loop(self):
        self.is_loop_active = True 
        while self.is_loop_active:
            for conn in self.connections:
                conn.check_events()

    def stop_loop(self):
        self.is_loop_active = False 
        for conn in self.connections:
            conn.disconnect()

    def register_conn(self, connection):
        conn = connectionThread(connection)
        self.connections.append(conn)

class PeerConnectionFailedError(Exception):
    pass

class connectionThread(threading.Thread):

    def __init__(self, peer):
        self.peer = peer 
        self.is_stopped = False
        self.receive_queue = Queue()
        self.write_queue = Queue()
        
        self.connect_event = threading.Event()
        self.disconnect_event = threading.Event()
        self.connection_succeeded = threading.Event()
        self.connection_failed = threading.Event()
        self.connection_lost = threading.Event()

        self.start()
        self.connect()

    def run(self):
        self.connect_event.wait()
        try:
            self.thread_connect()
        except PeerConnectionFailedError:
            self.connection_failed.set()
            self.sock.close()
            self.sock = None
            return

        while not self.disconnect_event.is_set():
            time.sleep(0)
            self.thread_send()
            self.thread_receive()

        self.sock.close()
        self.sock = None




def handle_connection(host, port):
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server
            s.connect((host, port))
            # Send data
            s.sendall(b'Hello, server!')
            # Receive data
            data = s.recv(1024)
            log.info(f"Received from {host}:{port}: {data.decode()}")
    except Exception as e:
        print(f"Error connecting to {host}:{port}: {e}")

def main():
    # Create threads for each connection
    threads = []
    for host, port in self.connections:
        t = threading.Thread(target=handle_connection, args=(host, port))
        threads.append(t)
        t.start()
    
    # Wait for all threads to finish
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
