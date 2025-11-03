import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b'Hello World'

print("UPD destination Ip: ",UDP_IP)
print("UDP destination Port:", UDP_PORT)
print("message:",str(MESSAGE,'utf-8'))

sock = socket.socket(socket.AF_INET, #IPv4
                     socket.SOCK_DGRAM) # Udp

sock.sendto(MESSAGE,(UDP_IP,UDP_PORT))
data,(ip,port) = sock.recvfrom(1024)
print("Message received:", str(data,'utf-8'))
time.sleep(1)
sock.close()

