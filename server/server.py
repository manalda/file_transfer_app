import socket
import variables
import tqdm
import os

SEPARATOR = ','
BUFFER_SIZE = 4096

server_socket = socket.socket()
server_socket.bind((variables.HOST, variables.PORT))
server_socket.listen(5)

client, address = server_socket.accept()
initial_message = server_socket.recv(BUFFER_SIZE).decode('utf-8')

user, file_name, file_size = initial_message.split(SEPARATOR)

with open(variables.ACCOUNTING_FILE, 'r') as f:
    users = f.readlines()

login_code = 0
for l in users:
    if user == l:
        login_code = 1
        break

client.send(login_code.to_bytes())

if login_code != 1:
    client.close()
    server_socket.close()
    #if login_code == 0 transfer is cancelled
else:
    file_name = os.path.basename(file_name)
    file_size = int(file_size)
    progress = tqdm.tqdm(range(file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
    
    f = open(file_name, 'wb')
    for _ in progress:
        bytes_read = client.recv(BUFFER_SIZE)
        if not bytes_read:    
            break

        f.write(bytes_read)
        progress.update(len(bytes_read))

    f.close()
    client.close()
    server_socket.close()