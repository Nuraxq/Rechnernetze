import argparse
import socket
import struct
from collections import defaultdict, deque

from database import Database

def get_avg(values):
    return sum(values)/len(values)

def main(ip,port):
    database = Database()
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((ip,port))
    arguments = ["temperatures","humidities","wind_speeds"]
    while(True):
        data, nadress = sock.recvfrom(1024)
        uid,seq,temp,hum,wind = struct.unpack("!HIfff",data)

        #Add User
        if not uid in database.get_present_uids():
            database.add_new_uid(uid)
        
        

        # First Packet initalising
        if database.getData(uid,"last_sequence_number") is None:
            database.add_data((uid,temp,hum,wind))
            database.set_last_sequence_number(uid,seq)
            
        # A Package we expect
        elif seq <= last_seq +1:
            last_seq = database.getData(uid,"last_sequence_number") 
            #Add Data
            database.add_data((uid,temp,hum,wind))
            if seq == last_seq +1:
                database.set_last_sequence_number(uid,seq)
            
            #Print Info
            averages = []
            for arg in arguments:
                averages.append(get_avg(database.getData(uid,arg)))
            print(f"Averages for client {uid}: {averages[0]}C | {averages[1]}% | {averages[2]}km/h")

        #Packages were Skipped 
        elif seq > (database.getData(uid,"last_sequence_number") +1):
            #Resend all lost Packages 
            for i in range(database.getData(uid,"last_sequence_number")+1,seq):
                response = struct.pack("!HI",uid,i)
                sock.sendto(response,nadress)
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WeatherStation UDP Server")
    parser.add_argument("--ip", default="127.0.0.1", help="IP address to bind the server")
    parser.add_argument("--port", default=4711, type=int, help="Port to bind the server")

    args = parser.parse_args()
    try:
        main(args.ip, args.port)
    except:
        pass
    finally:
        pass
