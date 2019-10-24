import socket
import time 
import random 
import argparse
from argparse import RawTextHelpFormatter

def parseArguments():
    parser = argparse.ArgumentParser(description='StopAndWait', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-v", "--version", action='version', version='')
    parser.add_argument("-ri", "--receiverip", required=True, help="Define receiver ip")
    parser.add_argument("-rp", "--receiverport", type=int, required=True, help="Define receiver port")

    return parser.parse_args()

# server_socket.settimeout(1)  

def main():
    args = parseArguments()
    dest = (args.receiverip, int(args.receiverport))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        server_socket.bind(dest)
        print('Server established!')
        print('Waiting for packages')   
    except:
        print('Error establishing server...')

        exit()
    while (True):
        acknowledged = False
        while True:
            data, adress = server_socket.recvfrom(512)
            number = random.randint(0, 100)
            if(number > 30 and acknowledged == False):
                server_socket.sendto(b'Acknowledged', adress)
                print("Received \'" + str(data, 'utf-8') + "\' with ACK")
                acknowledged = True
                break
            else:
                # server_socket.sendto(b'AKC', adress)
                print("Received \'" + str(data, 'utf-8') + "\', but could not send ACK")

if __name__ == "__main__":
    main()