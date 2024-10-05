import socket
from threading import Thread
import threading
from utility import *
from rich import print as rprint

HEADER = 64
PORT = 8888
SERVER_IP = get_local_ip()
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!BYE"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn:socket.socket, addr):
    rprint(f"[yellow]NEW CONNECTION : {addr[0]} connected[/yellow]")
    conn_active = True
    try:
        while conn_active:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MSG:
                    conn_active = False
                rprint(f"[magenta]{addr[0]}: {msg}[/magenta]")
        else:
            conn.close()
            rprint(f"[yellow]{addr[0]}: Exiting...[/yellow]")
    except Exception as e:
        rprint(f"[red]{addr[0]} {type(e).__name__}: {e}[/red]")
        conn.close()


def start_listening():
    try:
        rprint("[blue]Server is starting...[/blue]")
        server.listen()
        rprint(f"[green]Server is listening on {SERVER_IP}:{PORT}[/green]")
        while True:
            conn, addr = server.accept()
            thread = Thread(target=handle_client, args=(conn, addr,))
            thread.start()
            rprint(f"[green]ACTIVE CONNECTIONS : {threading.active_count() - 1}[/green]")
    except Exception as e:
        rprint(f"[red]{type(e).__name__}: ERROR STARTING SERVER {e}[/red]")


start_listening()