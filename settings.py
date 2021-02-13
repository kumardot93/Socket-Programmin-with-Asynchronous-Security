from decouple import config
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

#server_keys
private_key = "server_private_key.pem"
public_key = "server_public_key.pem"

# server host and port
SERVER_HOST = config("SERVER_HOST", cast=str, default="localhost")
SERVER_PORT = config("SERVER_PORT", cast=int, default=8000)

#crypto
def get_private_key():
    with open(config("SERVER_PRIVATE_KEY"), "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

def get_public_key():
    with open(config("SERVER_PUBLIC_KEY"), "rb") as key_file:
        return serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

server_public_key = get_public_key()
server_private_key = get_private_key()


