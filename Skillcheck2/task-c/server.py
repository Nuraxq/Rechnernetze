import argparse
import signal
import socket
import struct
import select

def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--port", default=4711, type=int, help="Port to listen for incoming connections")
    args = args_parser.parse_args()

    ########## Start your Code here ########## 
            
if __name__ == "__main__":
    main()

