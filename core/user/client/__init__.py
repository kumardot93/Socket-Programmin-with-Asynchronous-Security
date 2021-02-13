import sys
import settings
from core.utils.custom_logger import Log
from core.user.client.connection import create_connection
from core.utils.str_byte_conversion import str2bytes, bytes2str

def run_client():
    host = settings.SERVER_HOST
    port = settings.SERVER_PORT
    sock = create_connection((host, port))

    # Send data to server
    try:
        while True:
            # Input data to send
            orig_data = input("Enter data you want to send: ")

            sock.sendall(str2bytes(orig_data))

            while True:
                response = sock.recv(2048)
                while (len(response) > 0 and response.startswith(b'\0')):
                    response = response[1:]
                if (len(response) > 0):
                    break;                
            frames = bytes2str(response)
            if frames == "":
                continue
            Log.debug('Response: %s'% frames)

            

    except (KeyboardInterrupt, EOFError):
        sock.close()
        print()
        sys.exit(0)
