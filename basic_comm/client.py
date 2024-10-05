import socket
from rich import print as rprint
from utility import *
import os
import time

HEADER = 64
PORT = 8888
SERVER_IP = get_local_ip()
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!BYE"
IS_CONNECTED = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    try:
        encode_msg = str(msg).encode(FORMAT)
        message_length = len(encode_msg)
        message_length_encoded = f"{message_length}".encode(FORMAT)
        rprint(f"[blue]Message encoded length={message_length_encoded}[/blue]")
        if message_length < HEADER:
            message_length_encoded += b' ' * (HEADER - message_length)
        elif message_length > HEADER:
            rprint(f"[red]Length of {msg} is {message_length} more than {HEADER}[/red]")
            return
        rprint(f"[cyan]Sending length...[/cyan]")
        client.send(message_length_encoded)
        rprint(f"[green]Sending Messege...[/green]")
        client.send(encode_msg)
        time.sleep(1)
    except Exception as e:
        rprint(f"[red]{type(e).__name__}: {e}[/red]")

while IS_CONNECTED:
    os.system('cls')
    msg = input(f"Enter Message (DISCONNECT_MSG={DISCONNECT_MSG}): ")
    if msg == DISCONNECT_MSG:
        IS_CONNECTED = False
    send(msg)
else:
    client.close()