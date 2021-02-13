import threading
from core.utils.custom_logger import Log
from core.utils.str_byte_conversion import str2bytes, bytes2str

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

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server
    def run(self):
        while self.signal:
            try:
                if self.socket.sendall(b'\0') == 0:
                    raise ConnectionResetError
                frames = ""
                while True:
                    try:
                        chunk = self.socket.recv(2048)
                    except OSError:
                        break
                    frame = bytes2str(chunk)
                    frames += str(frame)  # put crypto code here
                if frames == "":
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
        # log("Client %s: '%s' bits received" % (str(self.id), self.frames), 2)
        # dec_data = server_physical(self.frames)
        # log("Client %s: '%s' bits decoded" % (str(self.id), dec_data), 2)
        # de_frame_data = server_dll(dec_data)

        # if de_frame_data != "":
        #     err_msg = "No error found."
        #     self.display("Decoded data from client: " + de_frame_data)
        # else:
        #     err_msg = "Error in data."
        return data

    def return_data(self, data):
        self.socket.sendall(str2bytes(data))

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
