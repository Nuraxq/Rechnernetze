import socket, struct

def main():
    IP = 'localhost'
    PORT = 4711
    sequence_number = 0
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.settimeout(1)

    with open("data.data","rb") as file:
        #TODO: schleife bis datei leer ist
        data = file.read(1024)

        while data:
            length = len(data)
            sendable = struct.pack("!cih",b"D",sequence_number,length)
            sendable += data
            tries = 0
            while tries < 10:
                sock.sendto(sendable,(IP,PORT))
                try:
                    print(f"Sending Chunk {sequence_number} to: {IP} {PORT}")
                    print(f"Currently on try:{tries} ")
                    response, nadress = sock.recvfrom(1024)
                    if len(response) == 5:
                
                        response_char, response_seq = struct.unpack("!ci",response)
                    
                        if(response_char == "A" and response_seq == sequence_number):
                            print(f" Got successfull answer on try {tries} for Chunk: {sequence_number}")
                            tries = 10 # Versuche 
                        else:  
                            print(f"Response to Chunk {sequence_number} on try {tries} was unsuccessful, retransmitting")
                            tries = tries +1
                    else:
                        print(f"Response to Chunk {sequence_number} on try {tries} was unsuccessful, retransmitting")
                        tries = tries +1

                except socket.timeout:
                    print(f"Response to Chunk {sequence_number} on try {tries} was unsuccessful, retransmitting")
                    tries = tries +1

            sequence_number = sequence_number +1
            data = file.read(1024)



    pass


if __name__ == "__main__":
    main()
