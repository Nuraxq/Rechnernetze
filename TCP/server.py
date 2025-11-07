import socket
import time
IP = 'localhost'
PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_STREAM) # TCP
sock.bind((IP, PORT))
sock.listen(5)
nsock, naddress = sock.accept()
print("received connection from: ", naddress)


while True:
    data = nsock.recv(1024)
    if not data:
        break
    print("Data: ",str(data,'utf-8'))
    time.sleep(1)
    nsock.sendall(data)
