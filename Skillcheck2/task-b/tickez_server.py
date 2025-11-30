import socket
import sys
import os
import struct
from typing import Optional, Tuple, Dict
from signal import signal, SIGCHLD, SIG_IGN, SIGINT
import argparse
import time


def parse_ticket_as_utf8EncodedString(filepath):
    """
    Reads a file from the predefined `FILEPATH`, encodes its content as UTF-8, and returns it.
    """
    ticket_content = ""
    if os.path.exists(filepath) and os.path.isfile(filepath):
        try:
            with open(filepath, 'r') as file:
                ticket_content = file.read().encode('utf8')
            return ticket_content
        except OSError as e:
            raise RuntimeError(f"Error reading file {filepath}: {e}")
    return b""


def signal_handler(signal_received, frame):
    global server_socket
    print("\nSIGINT received. Exiting...")
    if server_socket is not None:
        server_socket.close()
    sys.exit(0)


def check_port(port):
    """
    Checks if the port is in the allowed range
    """
    port = int(port)
    if port < 1023 or port > 65535:
        raise argparse.ArgumentTypeError("Port should be between 1024 and 65535")
    return int(port)


def main():
    signal(SIGINT, signal_handler)
    
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process port and dirpath arguments.")
    parser.add_argument("--port", type=check_port, default = 4711, help="Port number (1024-65535)")
    parser.add_argument("--dirpath", type=str, default="./tickets", help="File path to use, default is './tickets'.")
    args = parser.parse_args()

    # Validate dirpath
    if not os.path.isdir(args.dirpath):
        print("Ticket folder path not valid")
        sys.exit(-1)
    print(f"Port: {args.port}, Dirpath: {args.dirpath}")
    
    # --------- Start your Code here ----------- #
    # ...

    # Listen FD erstellen, der die Requests annimmt. 
    listenfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    listenfd.bind(('localhost',args.port))
    listenfd.listen(5)

    for i in range (0,4):
        pid = os.fork()
        if pid == 0:
            print(f"I am Child: {pid}")
            recv_request(listenfd)

def recv_request(lsock):
    while True:
        connectionfd , cadress = lsock.accept()
        treat_request(connectionfd)
        connectionfd.close()
    sys.exit()
        
def treat_request(connectionfd):
    data = connectionfd.recv(1024)
    namelen = struct.unpack("!H",data[:2])[0]
    name = data[2:2+namelen].decode("utf-8")
    path = f"tickets/{name}"
    
    filesize = os.path.getsize(path)
    filedata = parse_ticket_as_utf8EncodedString(path)
    fdatasize = len(filedata)

    first_response = struct.pack("!I",filesize) + data
    connectionfd.sendall(first_response)

    # --> Soll das hier so??? 
    # Wenn wir das verschicken ist es doch sowieso ein Bytes objekt, wieso 
    # sollten wir Bytes -> String -> Bytes kodieren. Unnötig. 
    
    second_response = struct.pack(f"!{fdatasize}s",filedata)
    connectionfd.sendall(second_response)

if __name__ == "__main__":
    main()
