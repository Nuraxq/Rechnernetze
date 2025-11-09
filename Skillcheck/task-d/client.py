import socket, struct

def main():
    IP = 'localhost'
    PORT = 4711

    sequence_number = 0

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    sock.settimeout(1)

    with open("data.data","rb") as file:
        data = file.read(1024)
        length = len(data)
        sendable = struct.pack("!cih",b"D",sequence_number,length)
        sendable += data





    pass


if __name__ == "__main__":
    main()
