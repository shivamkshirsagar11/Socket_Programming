import socket
import threading

FORMAT = 'utf-8'
PORT = 8888
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCON_MSG = "!discon"
HEADER = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

CLIENTS = set()

def broadcast(conn:socket.socket, msg:str):
    try:
        msg_encode = msg.encode(FORMAT)
        msg_len = len(msg_encode)
        msg_len_encode = str(msg_len).encode(FORMAT)
        if msg_len < HEADER:
            msg_len_encode += b' ' * (HEADER - msg_len)
        elif msg_len > HEADER:
            return 0
        for clients_socket in CLIENTS:
            if clients_socket != conn:
                clients_socket.send(msg_len_encode)
                clients_socket.send(msg_encode)
        return 1
    except Exception as e:
        if type(e).__name__ != "ConnectionResetError":
            print(f"Broadcast {type(e).__name__}: {e}")
        else:
            print(f"One connection is resetted...")
        return 1

def handle_client(conn:socket.socket, addr):
    try:
        connected = True
        while connected:
            msg_len = conn.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = conn.recv(msg_len).decode(FORMAT)
                if msg.split(": ")[1] == DISCON_MSG:
                    connected = False
                    msg = msg.split(": ")[0] + " is Leaving..."
                broadcast(conn, "\n\t\t\t\t"+msg)
        else:
            conn.close()
            CLIENTS.remove(conn)
    except Exception as e:
        print(f"{addr[0]} {type(e).__name__}: {e}")

def start_server():
    try:
        print("Server is starting...")
        server.listen()
        print(f"Server is listening on {SERVER}:{PORT}")

        while True:
            conn, addr = server.accept()
            CLIENTS.add(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr,))
            thread.start()
            print(f"Active Connections {threading.active_count() - 1}")
    except Exception as e:
        print(f"{addr[0]} {type(e).__name__}: {e}")

start_server()