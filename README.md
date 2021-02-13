# Socket-Programming-with-Asynchronous-Security

### Abstract
Data security is crucial in today's world. This project demonstrates how we can secure the data using asynchronous security. This project uses a client-server architecture. Both client and server generate a public and private key pair: the server stores both the key for further communication. During the handshaking, the client generates a public and private key and shares the public key with the server. In return, the server sends its public key. For all further communication, the server encrypts the data with the client's public key, and the client encrypts the data with the server's public. Thus only and server can understand the data sent by the client, and the client can understand the data sent by the server. Moreover, the server is a multithreaded server. The server initializes a new thread for every new connection. 

### Requirements
- Python3.6 or higher
- pipenv
- python-decouple
- cryptography

## Setup
- ***Make sure to activate the virtual environment and install all the dependencies***

To set up the project, run the following command.
```
cp .env.example .env
```
To initialize server's public and private key, run the following command.
```
python3 key-pair-init.py
```
To run the server, type the following command.
```
python3 manage.py server
```
To run the client, type the following command.
```
python3 manage.py client
```

