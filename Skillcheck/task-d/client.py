import socket,struct,time
def main():
    IP,PORT = 'localhost', 4711
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.settimeout(1)
    start = time.time()
    with open("data.data","rb") as file:
        data = file.read(1024)
        seq = 0
        while data:
            tries = 1
            length = len(data)
            while tries < 11:
                package = struct.pack("!cih",b"D",seq,length) + data
                sock.sendto(package,(IP,PORT))
                try:
                    ans,adr = sock.recvfrom(1024)
                    ansC ,ansSeq = struct.unpack("!ci",ans)
                    if(ansC == b'A' and ansSeq == seq):
                        print(f"[ACK]: Seq={seq} (attempt {tries}/10)")
                        seq = seq +1 # Seq Number erhöhen
                        tries = 11 # Schleife skippen
                    else:
                        print(f"Unexpected Answer: Seq={seq} (attempt {tries})")
                except socket.timeout:
                    print(f"[TIMEOUT] Seq={seq} (attempt {tries}/10)")
                tries = tries+1
            data = file.read(1024)

    total_time = (time.time() - start) * 1000
    finalize = struct.pack("!c",b'F')
    sock.sendto(finalize,(IP,PORT))
    print(f"Finalized {seq}/{seq} packets in {total_time} ms")
    sock.close()
    pass

if __name__ == "__main__":
    main()
