import socket
import settings
from core.utils.custom_logger import Log
from core.user.server.connection import new_connections


def run_server():
    # Get host and port
    host = settings.SERVER_HOST
    port = settings.SERVER_PORT

    # Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    Log.info("Server started on host %s and port %s" % (host, port))
    sock.listen(5)
    new_connections(sock)

