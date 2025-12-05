import struct,socket

def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind(('localhost',4711))
    while True:
        print("Session started!")
        with open("received.txt","a") as file:
            curr_client = None
            while True:
                data, adress = server.recvfrom(1024)

                if curr_client is None:
                    curr_client = adress
                    file.truncate(0)

                if curr_client != adress:
                    continue

                if len(data) == 1:
                    if data == b'F':
                        print("Received F byte, resetting State!")
                        break
                else:
                    char, length = struct.unpack("!cH",data[:3])
                    if char == b'D':
                        payload  = data[3:3+length]
                        lrc = data[3+length]

                        text = ""
                        for byte in payload:
                            text += chr((byte & 0b0111_1111))

                        if isValid(data[3:]):
                            file.write(text)
                            print(f"Text: {text} | Error: No")
                            server.sendto(b'A',curr_client)
                        else:
                            print(f"Text: {text} | Error: Yes")
                            server.sendto(b'E',curr_client)
    server.close()
    pass

def isValid(package: bytes):
    payload = package[:-1]
    lrc_byte = package[-1]
    for byte in package:
        if byte.bit_count() % 2 == 1:
            return False
    return lrc(payload,lrc_byte)

def lrc(data: bytes, lrc_byte):
    lrc = 0
    for byte in data:
        lrc ^= (byte & 0b0111_1111)
    return lrc == (lrc_byte & 0b0111_1111)

if __name__ == "__main__":
    main()
