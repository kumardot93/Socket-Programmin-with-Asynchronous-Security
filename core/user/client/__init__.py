import sys
import settings
from core.utils.custom_logger import Log
from core.user.client.connection import create_connection
from core.utils
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
                orig_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            Log.debug('encrypted data: ', encrypted)

            sock.sendall(str2bytes(encrypted))

            while True:
                response = sock.recv(32768)
                response = filterForNullTerminators(response)
                if (len(response) > 0):
                    break;                
            frames = bytes2str(response)
            if frames == "":
                continue

            decrypted_message = private_key.decrypt(
                frames,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            Log.debug('Response: %s'% decrypted_message)

            

    except (KeyboardInterrupt, EOFError):
        sock.close()
        print()
        sys.exit(0)
