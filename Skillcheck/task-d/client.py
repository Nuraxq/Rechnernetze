import socket, struct, time 

def main():
    IP = 'localhost'
    PORT = 4711
    sequence_number = 0
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.settimeout(1)

    with open("data.data","rb") as file:
        #TODO: schleife bis datei leer ist
        data = file.read(1024)
        start = time.time()
        while data:
            length = len(data)
            sendable = struct.pack("!cih",b"D",sequence_number,length)
            sendable += data
            tries = 1
            while tries < 11:
                sock.sendto(sendable,(IP,PORT))
                try:
                    print("----------------------------")
                    print(f"Sending Chunk {sequence_number} to: {IP} {PORT}")
                    print(f"Currently on try:{tries} ")
                    
                    response, nadress = sock.recvfrom(1024)
                    if len(response) == 5:
                
                        response_char, response_seq = struct.unpack("!ci",response)

                        if(response_seq == sequence_number and response_char == b'A'):
                            print(f"Got successfull answer on try {tries} for Chunk: {sequence_number}")
                            tries = 11 # Versuche 
                        else:  
                            print(f"Response to Chunk {sequence_number} on try {tries} was unsuccessful, retransmitting")
                            tries = tries +1
                    else:
                        print(f"Response to Chunk {sequence_number} on try {tries} was unsuccessful, retransmitting")
                        tries = tries +1

                except socket.timeout:
                    print(f"Response to Chunk {sequence_number} on try {tries} was unsuccessful, timer fail, retransmitting")
                    tries = tries +1

            sequence_number = sequence_number +1
            data = file.read(1024)
    
    finalize = struct.pack("!c",b"F")
    sock.sendto(finalize, (IP,PORT))
    endtime = time.time()
    ms_time = (endtime-start) * 1000
    print(f"Finalized 20/20 packets in {ms_time} ms time!")
    sock.close()
    pass


if __name__ == "__main__":
    main()
