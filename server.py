import socket
from threading import Thread
import threading
from utility import *

NUM_PORTS = 10
FREE_PORTS = get_free_ports(NUM_PORTS)
INDEX_GENERATOR = generator(NUM_PORTS)

PORT = FREE_PORTS[next(INDEX_GENERATOR)]
SERVER_IP = get_local_ip()
ADDR = (SERVER_IP, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn:socket.socket, addr):
    print(f"[NEW CONNECTION] : {addr} connected")
    conn_active = True
    
    while conn_active:
        msg = conn.recv()

def start_listening():
    print("[start_listening] Server is listening...")
    while True:
        conn, addr = server.accept()
        thread = Thread(target=handle_client, args=(conn, addr,))
        thread.start()
        print(f"[ACTIVE CONNECTIONs] : {threading.active_count() - 1}")