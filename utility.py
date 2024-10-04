import socket

def get_free_ports(num_ports=5):
    free_ports = []
    
    for _ in range(num_ports):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))  # Bind to an available port
            port = s.getsockname()[1]  # Get the assigned port
            free_ports.append(port)
    
    return free_ports

def generator(length):
    for i in range(length):
        yield i

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())
