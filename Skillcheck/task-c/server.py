import socket,struct 

def main():

    t = 0

    IP = 'localhost'
    PORT = 4711

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    sock.bind((IP,PORT))
    sock.listen(5)

    while True:
        nsock, nadress = sock.accept()

        while True:
            #Daten Empfangen
            data = nsock.recv(1024)
            #Falls Connection getrennt wurde
            if not data:
                break
            #Fallunterscheidung der Befehle
            if len(data) == 9:
                command,num = struct.unpack("!cd",data)
                num = float(num)
                if command == b'A':
                    t += num
                elif command == b'M':
                    t *= num
        
            elif len(data) == 1:
                command = struct.unpack("!c",data)[0]
                if command == b'R':
                    t = 0
                elif command == b'G':
                    package = struct.pack("!d",t)
                    nsock.sendall(package)
    pass


if __name__ == "__main__":
    main()
