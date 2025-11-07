import socket 
import struct
import time

def main():

    sec_num = 0 #Seq nummer die wir mitgeben
    number_rtt = 0 # RTT's mitzählen
    rttimes = [] 
    IP = 'localhost'
    PORT = 4711

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Socket aufsetzen
    sock.settimeout(3)

    while number_rtt < 11:
        data = struct.pack("!4si",b'PING',sec_num)
        try: 

            first = time.time() # Zeit messen

            sock.sendto(data,(IP,PORT)) # Daten verschicken

            answer, nadress  = sock.recvfrom(1024) # PONG erwarten

            second = time.time() # Zeit stoppen

            timediff = (second-first) * 1000 # Zeit in MS

            ansString, ansSeq = struct.unpack("4si",answer[0:8])

            if str(ansString,'utf-8') == "PONG":
                print(f"Seq {sec_num}: RTT ist {timediff}")

                rttimes.append(timediff)
                number_rtt = number_rtt +1

            else:
                print("Message doesnt begin with PONG")

        except socket.timeout:
            print(f"Message {sec_num} was lost")
                
        sec_num = sec_num + 1
    
    rttimes.sort()
    median = rttimes[len(rttimes)//2]
    print(f"Median der RTT's: {median}")

    sock.close()
    pass



if __name__ == "__main__":
    main()
