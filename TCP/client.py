import socket
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost',5005))
sock.send(b'Hello World')

time.sleep(3)
data = sock.recv(1024)

print("Data: ", str(data,'utf-8'))