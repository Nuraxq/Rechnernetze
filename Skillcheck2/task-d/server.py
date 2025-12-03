import socket, struct

def main():

    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind(('localhost',4711))
    print("Server Started")
    
    while True:
        print("New Session started!")

        with open("recieved.txt","w") as file:
            current_client = None
            while True:

                data, adress = server.recvfrom(1024)
                
                #Set client
                if current_client is None:
                    current_client = adress

                #Skip wrong client
                if current_client != adress:
                    continue

                #Data Packet
                if len(data) == 1:
                    if data == b'F':
                        print("Recieved finalize packet, resetting state")
                        break
                else:
                    char, length = struct.unpack("!ch",data[:3])

                    #Check for D, Split data
                    if char == b'D':
                        payload = data[3:3+length]
                        lrc_byte = data[3+length]
                        
                        #We only use lower 7 bits
                        text = ""
                        for zeichen in data:
                            text += chr(zeichen & 0b0111_1111)

                        if isValid(payload,lrc_byte):
                            print(f"Message: {text} | Error: No")
                            file.write(text)
                            server.sendto(b"A",(current_client))
                        else:
                            print(f"Message: {text} | Error: Yes") 
                            server.sendto(b"E",(current_client))

        
def isValid(payload, lrc_byte):
    for byte in payload:
        if not byteParity(byte):
            return False
    
    if not byteParity(lrc_byte):
        return False
    # Only use lower 7 bits of LRC byte    
    if lrc(payload) != (lrc_byte & 0b0111_1111) :
        print("hier")
        return False
    return True

def byteParity(data: int):
    return data.bits_count() % 2 == 0

def lrc(data: bytes):
    lrc = 0
    for byte in data:
        lrc ^= (byte & 0b0111_1111)
    return lrc

if __name__ == "__main__":
    main()
