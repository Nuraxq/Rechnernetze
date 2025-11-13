import struct, socket
def main():
    IP, PORT = 'localhost', 4711
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP,PORT))
    last_time = 0
    with open("temps.data") as file:
        for line in file:
            time,temp = int(line.split(' ')[0]),float(line.split(' ')[1])
            if(time-last_time >= 5000):
                sock.sendall(struct.pack("!qf",time,temp))
                last_time = time
    sock.close()
if __name__ == "__main__":
    main()
