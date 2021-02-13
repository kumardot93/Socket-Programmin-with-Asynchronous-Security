import sys
import settings
from core.utils.custom_logger import Log
from core.user.client.connection import create_connection
from core.utils.str_byte_conversion import str2bytes, bytes2str
from core.utils.dataOps import filterForNullTerminators
from core.user.client.handshaking import cryproHandShake
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def run_client():
    host = settings.SERVER_HOST
    port = settings.SERVER_PORT
    sock = create_connection((host, port))

    server_public_key, private_key = cryproHandShake(sock)

    # Send data to server
    try:
        while True:
            # Input data to send
            orig_data = input("Enter data you want to send: ")
            encrypted = server_public_key.encrypt(
                str2bytes(orig_data),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            Log.debug('encrypted data: %s'%encrypted)

            sock.sendall(encrypted)

            while True:
                response = sock.recv(32768)
                response = filterForNullTerminators(response)
                if (len(response) > 0):
                    break;                

            decrypted_message = private_key.decrypt(
                response,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            Log.debug('Response: %s'% bytes2str(decrypted_message))

            

    except (KeyboardInterrupt, EOFError):
        sock.close()
        print()
        sys.exit(0)
