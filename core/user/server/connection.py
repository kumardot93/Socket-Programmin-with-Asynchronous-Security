import threading
from core.utils.custom_logger import Log
from core.utils.str_byte_conversion import str2bytes, bytes2str
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from settings import server_private_key, server_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


# Variables for holding information about connections
connections = []
total_connections = 0


# Client class, new instance created for each connected client
# Each instance has the socket and address that is associated with items
# Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, sock, address, id_, name, signal):
        threading.Thread.__init__(self)
        self.socket = sock
        self.address = address
        self.id = id_
        self.name = name
        self.signal = signal
        self.error = False
        self.socket.settimeout(0.1)
        self.client_public_key = None

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    def handshaking(self):
        frames = b''
        while self.signal:
            while True:
                try:
                    chunk = self.socket.recv(32768)
                except OSError:
                    break
                frames += chunk  
            if len(frames) == 0:
                continue
            else:
                break
        
        self.client_public_key = serialization.load_pem_public_key(
            frames,
            backend=default_backend()
        )
        
        pem = server_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        self.socket.sendall(pem)
        

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server
    def run(self):
        self.handshaking()
        while self.signal:
            try:
                if self.socket.sendall(b'\0') == 0:
                    raise ConnectionResetError
                frames = b''
                while True:
                    try:
                        chunk = self.socket.recv(32768)
                    except OSError:
                        break
                    frames += chunk
                if len(frames) == 0:
                    continue
                data = self.decrypt_data(frames)
                self.display(data)
                self.return_data(data)
            except (ConnectionResetError, BrokenPipeError):
                Log.info("Client " + str(self.address) + " has disconnected")
                self.signal = False
                self.socket.close()
                connections.remove(self)
                break

    def decrypt_data(self, data):
        original_message = server_private_key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return bytes2str(original_message)

    def return_data(self, data):
        encrypted = self.client_public_key.encrypt(
            str2bytes(data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        self.socket.sendall(encrypted)

    def display(self, msg):
        Log.debug("Client " + str(self.id) + ": " + msg)


def new_connections(sock):
    try:
        while True:
            c_sock, address = sock.accept()
            global total_connections
            connections.append(Client(c_sock, address, total_connections, "Name", True))
            connections[len(connections) - 1].start()
            Log.debug("New connection at ID " + str(connections[len(connections) - 1]))
            total_connections += 1
    except (KeyboardInterrupt, EOFError):
        pass
