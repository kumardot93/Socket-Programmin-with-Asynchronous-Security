# Socket-Programmin-with-Asynchronous-Security

### Abstract
Data security is crucial in todays world. This project demonstrates how we can secure the data using asynchronous security. This projetc uses a client server srchitecture. Both clent and server generates a public and private key pair. The server stores both the key for all further communication. During the handshaking the clent generates a public and private key and shares the public key with server. In return server send its public key. For all further communication, server encrypts the data with client's public key and client encodes the data with server's public. Thus only and server can understand the data sent by client and client can understand the data sent by server. Moreover, the server is a multithreaded server. The server initiilzes a new thread for every new connection. 

### Requirements
- Python3.6 or higher
- pipenv
- python-decouple
- cryptography

## Setup
- ***Make sure to activate the virtual enviroment and install all the dependencies***

To setup the project, run the following command
```
cp .env.example .env
```
To initilize server's public and private key, run the following command
```
python3 key-pair-init.py
```
To run the server, type the following command
```
python3 manage.py server
```
To run the client, type the following command
```
python3 manage.py client
```

