import struct,socket,time

def main():

    IP = 'localhost'
    PORT = 4711
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.settimeout(3)
    samples, seq = [],0

    while len(samples) < 11:
        data = struct.pack("!4si",b"PING",seq_num)
        start = time.time()
        sock.sendto(data,(IP,PORT))
        try:
            ndata, naddress = sock.recvfrom(1024)
            rtt = (time.time() - start) * 1000
            answerS, answerSeq = struct.unpack("!4si",ndata)            
            if(answerSeq == seq_num and answerS == b'PONG'):
                print(f"Packet {seq_num} had a RTT of: {rtt} ms")
                samples.append(rtt)
            else:
                print("Wrong message Recieved")
        except socket.timeout:
            print(f"Packet {seq_num} had a timeout")
        seq_num = seq_num +1
        
    samples.sort()
    median = samples[5]
    print(f"Median over 11 RTT's is: {median}")
    sock.close()
    pass

if __name__ == "__main__":
    main()
