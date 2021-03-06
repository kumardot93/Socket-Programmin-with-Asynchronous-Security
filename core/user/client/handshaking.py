from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from core.utils.str_byte_conversion import str2bytes, bytes2str
from core.utils.dataOps import filterForNullTerminators
from core.utils.custom_logger import Log
import settings

def cryproHandShake(sock):
    private_key = rsa.generate_private_key( # new keys pair
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
    )

    public_key = private_key.public_key()

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    if settings.LogEncryptedData:
        Log.warning('client-public-key:')
        Log.warning(bytes2str(pem))

    sock.sendall(pem)

    while True:
        response = sock.recv(32768)
        response = filterForNullTerminators(response)
        if (len(response) > 0):
            break;
    
    if settings.LogEncryptedData:
        Log.warning('server public key:')
        Log.warning(bytes2str(response))

    server_public_key = serialization.load_pem_public_key(
        response,
        backend=default_backend()
    )

    return (server_public_key, private_key)   

