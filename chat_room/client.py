import socket
import threading

FORMAT = 'utf-8'
PORT = 8888
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCON_MSG = "!discon"
HEADER = 2048
IS_CONNECTED = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def recieve(conn:socket.socket):
    try:
        while IS_CONNECTED:
            msg_len = conn.recv(HEADER).decode(FORMAT)
            if msg_len:
                msg_len = int(msg_len)
                msg = conn.recv(msg_len).decode(FORMAT)
                print(msg)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")

def send(msg):
    try:
        encode_msg = str(msg).encode(FORMAT)
        message_length = len(encode_msg)
        message_length_encoded = f"{message_length}".encode(FORMAT)
        if message_length < HEADER:
            message_length_encoded += b' ' * (HEADER - message_length)
        elif message_length > HEADER:
            return
        client.send(message_length_encoded)
        client.send(encode_msg)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")

thread = threading.Thread(target=recieve, args=(client,))
thread.start()
client_name = input("Enter your name: ")
print(f"For exiting type {DISCON_MSG}")
while IS_CONNECTED:
    msg = client_name + ": "+ input()
    if msg.count(DISCON_MSG) == 1:
        IS_CONNECTED = False
    send(msg)
else:
    client.close()
    thread.join()