import socket
import variables
import tqdm
import os

SEPARATOR = ','
BUFFER_SIZE = 4096

server_socket = socket.socket()