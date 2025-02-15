import socket
import tqdm
import variables
import sys
import os
from zipfile import ZipFile

SEPARATOR = ','
BUFFER_SIZE = 4096

if len(sys.argv) != 2:
    print("Usage: python3 <file_name>")
    sys.exit(-1)

file_name = str(sys.argv[1])

user = input("Usuario: ")

if not os.path.exists(file_name):
    print("File {0} does not exists".format(file_name))
    sys.exit(-2)


file_size = os.path.getsize(file_name)

client_socket = socket.socket()
client_socket.connect((variables.SERVER_HOST, variables.SERVER_PORT))

message = f"{user}{SEPARATOR}{file_name}{SEPARATOR}{file_size}"
client_socket.send(message.encode('utf-8'))
login_code = client_socket.recv(BUFFER_SIZE).decode('utf-8')

"""login codes: 
    [ERROR] user does not exist
    [OK] login was successful
"""
if login_code != "OK":
    print("User {0} does not exist".format(user))
    sys.exit(-3)

zip_name = "send.zip"
zip_file = ZipFile(zip_name, 'w')
zip_file.write(file_name)
zip_file.close()

f = open(zip_name, 'rb')
progress = tqdm.tqdm(range(file_size), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
for _ in progress:
    bytes_read = f.read(BUFFER_SIZE)
    if not bytes_read:
        break
  
    client_socket.sendall(bytes_read)
    progress.update(len(bytes_read))

f.close()
client_socket.close()