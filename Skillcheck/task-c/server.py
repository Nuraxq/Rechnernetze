import struct, socket
def main():
    IP,PORT = 'localhost',4711
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind((IP,PORT))
    sock.listen(5)
    t = 0.0
    while True:
        nsock , nadress = sock.accept()
        while True:
            data = nsock.recv(1024)
            if not data: 
                nsock.close()
                break
            if len(data) == 9:
                com,num = struct.unpack("!cd",data)
                if com == b'A':
                    t += num
                elif com == b'M':
                    t *= num
            elif len(data) == 1:
                com = struct.unpack("!c",data)[0] # unpack gibt tupel zurück
                if com == b'R':
                    t = 0
                elif com == b'G':
                    nsock.sendall(struct.pack("!d",t))
    pass
if __name__ == "__main__":
    main()
