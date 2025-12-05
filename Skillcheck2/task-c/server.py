import argparse
import signal
import socket
import struct
import select

def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--port", default=4711, type=int, help="Port to listen for incoming connections")
    args = args_parser.parse_args()

    totals = {}
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind(('localhost',args.port))
    server.listen(5)
    slist = []
    slist.append(server)
    totals = {}
    while True:
        readable,writeable,error = select.select(slist,[],[],0) # <- 0 am Ende!
        for sock in readable:
            if sock == server:
                nsock,address = server.accept()
                slist.append(nsock)
            else:
                data = sock.recv(1024)
                if not data:
                    if sock in slist:
                        slist.remove(sock)
                    continue
        
                address = sock.getpeername()
                if address not in totals:
                    totals[address] = 0
                    
                if len(data) == 1:
                    if data == b'R':
                        totals[address] = 0
                    elif data == b'G':
                        sock.sendall(struct.pack("!d",totals[address]))
                        
                elif len(data) == 9:
                    char, num = struct.unpack("!cd",data)
                    if char == b'A':
                       totals[address] += num
                    elif char == b'M':
                        totals[address] *= num 
    for sock in slist:
        sock.close()

if __name__ == "__main__":
    main()

