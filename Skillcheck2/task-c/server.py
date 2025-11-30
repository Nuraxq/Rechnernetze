import argparse
import signal
import socket
import struct
import select

def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--port", default=4711, type=int, help="Port to listen for incoming connections")
    args = args_parser.parse_args()

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("127.0.0.1",args.port))
    server.listen(5)
    socketlist = []
    socketlist.append(server)

    totals = {}

    while True:
        readable,writeable,error = select.select(socketlist,[],[],0)

        for sock in readable:
            if sock == server:
                sockfd, addr = server.accept()
                socketlist.append(sockfd)

            else:
                data = sock.recv(1024)  
                adress = sock.getpeername()
                if adress not in totals:
                    totals[adress] = 0
                if not data:
                    if sock in socketlist:
                        socketlist.remove(sock)
                        continue


                if len(data) == 9:
                    char, num = struct.unpack("!cd",data)
                    if char == b'A':
                        totals[adress] = totals[adress] + num
                    elif char == b'M':
                        totals[adress] = totals[adress] * num
                elif len(data) == 1:
                    char = struct.unpack("!c",data)[0]
                    if char == b'G':
                        sock.sendall(struct.pack("!d",totals[adress]))
                    elif char == b'R':
                        totals[adress] = 0
    for sock in socketlist:
        sock.close()
    server.close()



            
if __name__ == "__main__":
    main()

