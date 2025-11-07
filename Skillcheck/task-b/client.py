import socket
import struct

def main():
    
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    IP = 'localhost'
    PORT = 4711

    sock.connect((IP,PORT))

    last_time = 0    
    byteString = b''

    with open("temps.data",'rt') as file:
        for line in file:
            time, temp = line.split(' ')
            time = int(time)
            temp = float(temp)
        
            if time - last_time >= 5000:
                byteString += struct.pack("!qf",time,temp)
                last_time = time
             
        sock.sendall(byteString)
    
    sock.close()
    pass


if __name__ == "__main__":
    main()
