import argparse
import socket
import struct
from collections import defaultdict, deque

from database import Database

def get_avg(values):
    return sum(values)/len(values)

def main(ip,port):
    database = Database()

    # ------- Start cour code here ------- #
    # ...

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
