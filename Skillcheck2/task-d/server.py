import socket, struct


def main():

    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind(('localhost',4711))

    # Goofy doppel schleife überarbeiten!
    while True:
        data,adress = server.recvfrom(1024)
        ch, len = struct.unpack("!cH",data[:3])
        if (ch == b'D'):
            curr_client = adress
            session_active = True
        while session_active:
            with open("recieved.txt","wt") as file:



    


def byteParity(data: bytes):



def lrc(data: bytes):
    lrc = 0
    for byte in data:
        lrc ^= byte
    return lrc

if __name__ == "__main__":
    main()
