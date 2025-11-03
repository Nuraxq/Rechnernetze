import socket

UDP_IP = 'localhost'
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, #IPv4
                     socket.SOCK_DGRAM) #UDP

sock.bind((UDP_IP,UDP_PORT))


while True:
        data, (ip,port) = sock.recvfrom(1024)

        print("message recieved: ", str(data,'utf-8'))
        print("from: ",ip)
        print("on port: ",port)
        sock.sendto(b'67',(ip,port))
