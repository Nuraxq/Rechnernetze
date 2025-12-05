import argparse
import socket
import struct
from collections import defaultdict, deque

from database import Database

def get_avg(values):
    return sum(values)/len(values)

def main(ip,port):
    database = Database()

    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind((ip,port))
    arguments = ["temperatures","humidities","wind_speeds"]
    while True:
        data, adress = server.recvfrom(1024)
        uid,seq,temp,hum,wind = struct.unpack("!HIfff",data)
        
        if uid not in database.get_present_uids():
            database.add_new_uid(uid)
        
        if database.getData(uid,"last_sequence_number") is None:
            database.set_last_sequence_number(uid,seq)
        
        last_seq = database.getData(uid,"last_sequence_number")

        if seq > last_seq +1:
            for i in range(last_seq+1,seq):
                server.sendto((struct.pack("!HI",uid,i)),adress)
        
        database.add_data(uid,temp,hum,wind)
        if seq > last_seq:
            database.set_last_sequence_number(uid,seq)

        averages = []
        for arg in arguments:
            averages.append(get_avg(database.getData(uid,arg)))
        print(f"User: {uid} | Temp: {averages[0]} | Hum: {averages[1]} | Wind: {averages[2]}")
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
