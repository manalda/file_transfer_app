import socket
from zipfile import ZipFile
import variables
import tqdm
import os

SEPARATOR = ','
BUFFER_SIZE = 4096

while True:
    server_socket = socket.socket()
    server_socket.bind((variables.HOST, variables.PORT))
    server_socket.listen(5)
    print("Waiting for connections...")

    client, address = server_socket.accept()
    print("Connection established")

    initial_message = client.recv(BUFFER_SIZE).decode('utf-8')

    user, file_name, file_size = initial_message.split(SEPARATOR)

    with open(variables.ACCOUNTING_FILE, 'r') as f:
        users = f.readlines()

    login_code = "ERROR"
    for l in users:
        if user == l:
            login_code = "OK"
            break

    client.send(login_code.encode('utf-8'))

    if login_code != "OK":
        print("User is incorrect. Closing connection...")
        client.close()
        server_socket.close()
        print("Connection closed.")
        continue
    else:
        print("Receiving file...")
        file_name = os.path.basename(file_name)
        file_size = int(file_size)
        progress = tqdm.tqdm(range(file_size), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
        zip_name = "received.zip"

        f = open(zip_name, 'wb')
        for _ in progress:
            bytes_read = client.recv(BUFFER_SIZE)
            if not bytes_read:    
                break

            f.write(bytes_read)
            progress.update(len(bytes_read))

        f.close()
        zip_file = ZipFile(zip_name, 'r')
        zip_file.extractall()
        zip_file.close()

        client.close()
        server_socket.close()
        print("File received. Connection closed.")